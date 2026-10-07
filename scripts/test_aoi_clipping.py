from pathlib import Path

from src.data.preparation import clip_raster_to_aoi


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw" / "sentinel2"
AOI_DIR = PROJECT_ROOT / "data" / "aoi"
OUTPUT_DIR = PROJECT_ROOT / "data" / "interim" / "sentinel2" / "aoi_test"


# Recherche du B04 déjà téléchargé
b04_files = list(RAW_DIR.rglob("*B04_10m.jp2"))

if not b04_files:
    raise FileNotFoundError(
        "Aucun fichier B04_10m.jp2 trouvé dans data/raw/sentinel2"
    )

input_path = b04_files[0]

print("Raster source :", input_path)


for name in ["libreville", "akanda", "owendo"]:

    print(f"\n--- {name.upper()} ---")

    aoi_path = AOI_DIR / f"{name}.geojson"

    output_path = (
        OUTPUT_DIR
        / name
        / f"{name}_B04_10m.tif"
    )

    result = clip_raster_to_aoi(
        input_path=input_path,
        output_path=output_path,
        aoi_path=aoi_path,
    )

    print("Découpage OK :", result)