from pathlib import Path

import numpy as np
import rasterio

from src.data.preparation import (
    clip_raster_to_aoi,
    mask_ndvi_with_scl,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "sentinel2"
AOI_PATH = PROJECT_ROOT / "data" / "aoi" / "libreville.geojson"

NDVI_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "sentinel2"
    / "ndvi_test"
    / "libreville"
)

NDVI_PATH = NDVI_DIR / "libreville_NDVI.tif"
SCL_PATH = NDVI_DIR / "libreville_SCL_20m.tif"
OUTPUT_PATH = NDVI_DIR / "libreville_NDVI_clean.tif"


# Recherche du SCL du produit Sentinel-2
scl_files = list(
    RAW_DIR.rglob("*SCL_20m.jp2")
)

if not scl_files:
    raise FileNotFoundError(
        "Aucun fichier SCL_20m trouvé."
    )


# Découpage du SCL avec la même AOI
clip_raster_to_aoi(
    input_path=scl_files[0],
    output_path=SCL_PATH,
    aoi_path=AOI_PATH,
)


# Application du masque
mask_ndvi_with_scl(
    ndvi_path=NDVI_PATH,
    scl_path=SCL_PATH,
    output_path=OUTPUT_PATH,
)


# Contrôle qualité
with rasterio.open(OUTPUT_PATH) as src:
    ndvi = src.read(1)

valid = ~np.isnan(ndvi)

print("NDVI nettoyé :", OUTPUT_PATH)
print("Dimensions :", ndvi.shape)

print(
    "Pixels valides :",
    np.count_nonzero(valid),
    "/",
    ndvi.size,
)

print(
    "Part valide :",
    round(
        np.count_nonzero(valid)
        / ndvi.size
        * 100,
        2,
    ),
    "%",
)

print(
    "NDVI moyen :",
    float(np.nanmean(ndvi)),
)

print(
    "Minimum :",
    float(np.nanmin(ndvi)),
)

print(
    "Maximum :",
    float(np.nanmax(ndvi)),
)