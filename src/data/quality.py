"""Contrôles de qualité des données à développer."""
from pathlib import Path

import numpy as np
import rasterio


INVALID_SCL_CLASSES = {
    0,   # No data
    1,   # Saturated / defective
    3,   # Cloud shadows
    8,   # Clouds medium probability
    9,   # Clouds high probability
    10,  # Thin cirrus
    11,  # Snow / ice
}


def calculate_scl_quality(
    scl_path: Path,
) -> dict:
    """Calculate Sentinel-2 quality indicators from an AOI-clipped SCL."""

    with rasterio.open(scl_path) as src:
        scl = src.read(1)

    total_pixels = scl.size

    water_mask = scl == 6

    invalid_mask = np.isin(
        scl,
        list(INVALID_SCL_CLASSES),
    )

    data_mask = scl != 0

    land_mask = data_mask & ~water_mask

    # Pixels terrestres qui ne sont ni nuages,
    # ni ombres, ni données invalides
    valid_land_mask = land_mask & ~invalid_mask

    land_pixels = np.count_nonzero(land_mask)
    water_pixels = np.count_nonzero(water_mask)
    invalid_pixels = np.count_nonzero(invalid_mask)
    valid_land_pixels = np.count_nonzero(valid_land_mask)

    # Qualité utile pour une analyse terrestre
    if land_pixels > 0:
        usable_land_percent = (
            valid_land_pixels
            / land_pixels
            * 100
        )
    else:
        usable_land_percent = 0.0

    return {
        "total_pixels": total_pixels,
        "land_pixels": land_pixels,
        "water_percent": water_pixels / total_pixels * 100,
        "invalid_percent": invalid_pixels / total_pixels * 100,
        "usable_land_pixels": valid_land_pixels,
        "usable_land_percent": usable_land_percent,
    }