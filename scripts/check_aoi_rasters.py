from pathlib import Path
import rasterio


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BASE_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "sentinel2"
    / "aoi_test"
)


for name in ["libreville", "akanda", "owendo"]:

    raster_path = (
        BASE_DIR
        / name
        / f"{name}_B04_10m.tif"
    )

    with rasterio.open(raster_path) as src:

        print(f"\n--- {name.upper()} ---")
        print("CRS :", src.crs)
        print("Dimensions :", src.width, "x", src.height)
        print("Résolution :", src.res)
        print("Nombre de bandes :", src.count)
        print("Type :", src.dtypes[0])