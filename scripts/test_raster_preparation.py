from pathlib import Path
from src.data.preparation import (
    clip_rgb_bands,
    create_rgb_array,
    inspect_raster,
)
from src.data.preparation import inspect_raster
import matplotlib.pyplot as plt
import rasterio

RASTER_PATH = Path(
    "data/raw/sentinel2/"
    "S2B_MSIL2A_20250115T093239_N0511_R136_T32NNF_20250115T120528/"
    "T32NNF_20250115T093239_B04_10m.jp2"
)

PRODUCT_DIR = Path(
    "data/raw/sentinel2/"
    "S2B_MSIL2A_20250115T093239_N0511_R136_T32NNF_20250115T120528"
)

RGB_OUTPUT_DIR = Path(
    "data/interim/sentinel2/test_area"
)

def main():
    metadata = inspect_raster(RASTER_PATH)

    print("\nMétadonnées raster")

    for key, value in metadata.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()

from pathlib import Path

from src.data.preparation import (
    clip_raster,
    inspect_raster,
)


RASTER_PATH = Path(
    "data/raw/sentinel2/"
    "S2B_MSIL2A_20250115T093239_N0511_R136_T32NNF_20250115T120528/"
    "T32NNF_20250115T093239_B04_10m.jp2"
)

OUTPUT_PATH = Path(
    "data/interim/sentinel2/test_area/B04_10m.tif"
)

BBOX = (9.40, 0.30, 9.50, 0.40)


def main():
    print("Raster RAW")
    raw_metadata = inspect_raster(RASTER_PATH)

    print(
        f"{raw_metadata['width']} x "
        f"{raw_metadata['height']} pixels"
    )

    output_path = clip_raster(
        input_path=RASTER_PATH,
        output_path=OUTPUT_PATH,
        bbox=BBOX,
    )

    print("\nRaster découpé")
    clipped_metadata = inspect_raster(output_path)

    with rasterio.open(output_path) as src:
        band = src.read(1)

    plt.imshow(band, cmap="gray")
    plt.title("Sentinel-2 B04 - Zone test GEONAF")
    plt.colorbar(label="Réflectance")
    plt.show()

    for key, value in clipped_metadata.items():
        print(f"{key}: {value}")

    rgb_bands = clip_rgb_bands(
        product_dir=PRODUCT_DIR,
        output_dir=RGB_OUTPUT_DIR,
        bbox=BBOX,
    )

    rgb = create_rgb_array(
        red_path=rgb_bands["B04"],
        green_path=rgb_bands["B03"],
        blue_path=rgb_bands["B02"],
    )

    plt.figure(figsize=(10, 10))
    plt.imshow(rgb)
    plt.title("GEONAF - Sentinel-2 RGB")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()



