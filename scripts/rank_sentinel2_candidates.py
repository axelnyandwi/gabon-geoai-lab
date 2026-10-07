from pathlib import Path

import boto3

from src.config import (
    CDSE_S3_ACCESS_KEY,
    CDSE_S3_SECRET_KEY,
    CDSE_S3_ENDPOINT,
)
from src.data.ingestion import (
    search_sentinel2,
    get_asset,
    download_asset,
)
from src.data.preparation import clip_raster_to_aoi
from src.data.quality import calculate_scl_quality


PROJECT_ROOT = Path(__file__).resolve().parents[1]

AOI_PATH = (
    PROJECT_ROOT
    / "data"
    / "aoi"
    / "libreville.geojson"
)

CACHE_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "sentinel2_quality"
)

INTERIM_DIR = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "sentinel2_quality"
)


# Même bbox utilisée lors de notre recherche précédente
BBOX = [
    9.3674836,
    0.3414472,
    9.5273529,
    0.5638127,
]


# 1. Recherche des candidats
items = search_sentinel2(
    bbox=BBOX,
    start_date="2025-01-01",
    end_date="2025-01-31",
)

print(f"Produits trouvés : {len(items)}")


# 2. Client S3
if not CDSE_S3_ACCESS_KEY or not CDSE_S3_SECRET_KEY:
    raise RuntimeError(
        "Credentials CDSE S3 absents des variables d'environnement."
    )

s3_client = boto3.client(
    "s3",
    endpoint_url=CDSE_S3_ENDPOINT,
    aws_access_key_id=CDSE_S3_ACCESS_KEY,
    aws_secret_access_key=CDSE_S3_SECRET_KEY,
    region_name="default",
)


results = []


for item in items:

    product_id = item["id"]

    cloud_cover = item.get(
        "properties",
        {},
    ).get("eo:cloud_cover")

    print(f"\nAnalyse : {product_id}")
    print(f"Nuages STAC : {cloud_cover}")

    try:
        # 1. Récupération du SCL uniquement
        asset = get_asset(
            item,
            "SCL_20m",
        )

        raw_dir = (
            CACHE_DIR
            / product_id
        )

        scl_path = download_asset(
            s3_client=s3_client,
            asset=asset,
            destination_dir=raw_dir,
        )

        # 2. Découpage sur l'AOI
        clipped_path = (
            INTERIM_DIR
            / product_id
            / "libreville_SCL_20m.tif"
        )

        clip_raster_to_aoi(
            input_path=scl_path,
            output_path=clipped_path,
            aoi_path=AOI_PATH,
        )

        # 3. Calcul de qualité
        quality = calculate_scl_quality(
            clipped_path
        )

        usable = quality[
            "usable_land_percent"
        ]

        print(
            f"Terrain exploitable : "
            f"{usable:.2f} %"
        )

        results.append(
            {
                "product_id": product_id,
                "cloud_cover": cloud_cover,
                "usable_land_percent": usable,
            }
        )

    except Exception as error:

        print(
            f"ÉCHEC : {product_id}"
        )

        print(
            f"Raison : {error}"
        )

        continue


# 6. Classement
results.sort(
    key=lambda x: x["usable_land_percent"],
    reverse=True,
)


print("\n==============================")
print("CLASSEMENT GEONAF - LIBREVILLE")
print("==============================")

for rank, result in enumerate(
    results,
    start=1,
):

    print(
        f"{rank}. "
        f"{result['product_id']}"
    )

    print(
        f"   STAC cloud cover : "
        f"{result['cloud_cover']}"
    )

    print(
        f"   Terrain exploitable : "
        f"{result['usable_land_percent']:.2f} %"
    )