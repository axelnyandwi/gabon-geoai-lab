"""Acquisition et mise à jour des données géospatiales à développer."""
from pathlib import Path


def get_asset(item: dict, asset_name: str) -> dict:
    """Return an asset from a STAC item."""

    asset = item.get("assets", {}).get(asset_name)

    if asset is None:
        raise ValueError(f"Asset introuvable : {asset_name}")

    return asset

def get_s3_key(asset: dict, bucket_name: str = "eodata") -> str:
    """Extract the object key from an S3 asset."""

    s3_uri = asset.get("href")

    if not s3_uri:
        raise ValueError("L'asset ne contient pas de href.")

    prefix = f"s3://{bucket_name}/"

    if not s3_uri.startswith(prefix):
        raise ValueError(f"URI S3 inattendue : {s3_uri}")

    return s3_uri.removeprefix(prefix)

def download_asset(
    s3_client,
    asset: dict,
    destination_dir: Path,
    bucket_name: str = "eodata",
) -> Path:
    """Download an S3 asset locally if it is not already cached."""

    s3_key = get_s3_key(asset, bucket_name)

    destination_dir.mkdir(parents=True, exist_ok=True)

    local_path = destination_dir / Path(s3_key).name

    if local_path.exists():
        return local_path

    s3_client.download_file(
        bucket_name,
        s3_key,
        str(local_path),
    )

    return local_path

import requests


def search_sentinel2(
    bbox: list[float],
    start_date: str,
    end_date: str,
    max_cloud_cover: float | None = None,
) -> list[dict]:
    """Search Sentinel-2 L2A products from the CDSE STAC API."""

    url = "https://stac.dataspace.copernicus.eu/v1/search"

    payload = {
        "collections": ["sentinel-2-l2a"],
        "bbox": bbox,
        "datetime": f"{start_date}T00:00:00Z/{end_date}T23:59:59Z",
        "limit": 100,
    }

    if max_cloud_cover is not None:
        payload["query"] = {
            "eo:cloud_cover": {
                "lte": max_cloud_cover
            }
        }
        
    response = requests.post(
        url,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    return data.get("features", [])

def select_best_product(items: list[dict]) -> dict:
    """Select the Sentinel-2 product with the lowest cloud cover."""

    if not items:
        raise ValueError("Aucun produit Sentinel-2 disponible.")

    return min(
        items,
        key=lambda item: item.get("properties", {}).get(
            "eo:cloud_cover",
            float("inf"),
        ),
    )