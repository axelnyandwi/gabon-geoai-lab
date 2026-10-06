from pathlib import Path

from src.data.ingestion import (
    create_cdse_s3_client,
    ingest_sentinel2_product,
)


BBOX = [9.40, 0.30, 9.50, 0.40]

OUTPUT_DIR = Path("data/raw/sentinel2")


def main():
    s3_client = create_cdse_s3_client()

    result = ingest_sentinel2_product(
        s3_client=s3_client,
        bbox=BBOX,
        start_date="2025-01-01",
        end_date="2025-01-31",
        destination_dir=OUTPUT_DIR,
        max_cloud_cover=50,
        asset_names=[
            "B02_10m",
            "B03_10m",
            "B04_10m",
        ],
    )

    print("\nIngestion terminée")
    print("Produit :", result["product_id"])
    print("Répertoire :", result["directory"])

    for asset_name, path in result["assets"].items():
        size_mb = path.stat().st_size / (1024 * 1024)

        print(
            f"{asset_name} : {path} "
            f"({size_mb:.1f} Mo)"
        )


if __name__ == "__main__":
    main()