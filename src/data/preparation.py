"""Préparation et harmonisation des données à développer."""
"""Preparation and transformation of geospatial raster data."""

from pathlib import Path
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds

import rasterio
import numpy as np

def inspect_raster(raster_path: Path) -> dict:
    """Read the main metadata of a raster file."""

    if not raster_path.exists():
        raise FileNotFoundError(f"Raster introuvable : {raster_path}")

    with rasterio.open(raster_path) as dataset:
        return {
            "path": raster_path,
            "width": dataset.width,
            "height": dataset.height,
            "bands": dataset.count,
            "dtype": dataset.dtypes[0],
            "crs": dataset.crs.to_string() if dataset.crs else None,
            "resolution": dataset.res,
            "bounds": dataset.bounds,
            "nodata": dataset.nodata,
        }

def clip_raster_to_bbox(
    input_path: Path,
    output_path: Path,
    bbox: tuple[float, float, float, float],
) -> Path:
    """Clip a raster using a bounding box expressed in the raster CRS."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(input_path) as src:
        window = from_bounds(
            *bbox,
            transform=src.transform,
        )

        data = src.read(window=window)

        transform = src.window_transform(window)

        profile = src.profile.copy()
        profile.update(
            width=data.shape[2],
            height=data.shape[1],
            transform=transform,
        )

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(data)

    return output_path

def transform_bbox(
    bbox: tuple[float, float, float, float],
    source_crs: str,
    target_crs: str,
) -> tuple[float, float, float, float]:
    """Transform a bounding box between coordinate reference systems."""

    return transform_bounds(
        source_crs,
        target_crs,
        *bbox,
    )

def clip_raster(
    input_path: Path,
    output_path: Path,
    bbox: tuple[float, float, float, float],
    bbox_crs: str = "EPSG:4326",
) -> Path:
    """Clip a raster from a bbox and automatically handle CRS conversion."""

    with rasterio.open(input_path) as src:
        if src.crs is None:
            raise ValueError(
                f"Le raster ne possède pas de CRS : {input_path}"
            )

        raster_crs = src.crs.to_string()

    raster_bbox = transform_bbox(
        bbox=bbox,
        source_crs=bbox_crs,
        target_crs=raster_crs,
    )

    return clip_raster_to_bbox(
        input_path=input_path,
        output_path=output_path,
        bbox=raster_bbox,
    )

def clip_rgb_bands(
    product_dir: Path,
    output_dir: Path,
    bbox: tuple[float, float, float, float],
) -> dict[str, Path]:
    """Clip the Sentinel-2 RGB bands to the same area."""

    band_patterns = {
        "B02": "*_B02_10m.jp2",
        "B03": "*_B03_10m.jp2",
        "B04": "*_B04_10m.jp2",
    }

    outputs = {}

    for band_name, pattern in band_patterns.items():
        matches = list(product_dir.glob(pattern))

        if len(matches) != 1:
            raise ValueError(
                f"Attendu 1 fichier pour {band_name}, "
                f"trouvé : {len(matches)}"
            )

        output_path = output_dir / f"{band_name}_10m.tif"

        outputs[band_name] = clip_raster(
            input_path=matches[0],
            output_path=output_path,
            bbox=bbox,
        )

    return outputs

def normalize_band(
    band: np.ndarray,
    lower_percentile: float = 2,
    upper_percentile: float = 98,
) -> np.ndarray:
    """Normalize a satellite band for visualization."""

    valid_pixels = band[band > 0]

    if valid_pixels.size == 0:
        return np.zeros_like(band, dtype=np.float32)

    low, high = np.percentile(
        valid_pixels,
        [lower_percentile, upper_percentile],
    )

    if high <= low:
        return np.zeros_like(band, dtype=np.float32)

    normalized = (band.astype(np.float32) - low) / (high - low)

    return np.clip(normalized, 0, 1)

def create_rgb_array(
    red_path: Path,
    green_path: Path,
    blue_path: Path,
) -> np.ndarray:
    """Create a natural-color RGB array from Sentinel-2 bands."""

    with rasterio.open(red_path) as src:
        red = src.read(1)

    with rasterio.open(green_path) as src:
        green = src.read(1)

    with rasterio.open(blue_path) as src:
        blue = src.read(1)

    if red.shape != green.shape or red.shape != blue.shape:
        raise ValueError(
            "Les bandes RGB n'ont pas les mêmes dimensions."
        )

    red = normalize_band(red)
    green = normalize_band(green)
    blue = normalize_band(blue)

    return np.dstack((red, green, blue))