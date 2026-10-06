"""Acquisition et mise à jour des données géospatiales à développer."""
import os

import boto3
import requests
from dotenv import load_dotenv
from pathlib import Path


def create_cdse_s3_client():
    """Create an authenticated S3 client for Copernicus Data Space."""

    load_dotenv()

    access_key = os.getenv("CDSE_S3_ACCESS_KEY")
    secret_key = os.getenv("CDSE_S3_SECRET_KEY")

    if not access_key or not secret_key:
        raise ValueError(
            "Variables CDSE_S3_ACCESS_KEY et CDSE_S3_SECRET_KEY manquantes."
        )

    return boto3.client(
        "s3",
        endpoint_url="https://eodata.dataspace.copernicus.eu",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="default",
    )

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

def ingest_sentinel2_product(
    s3_client,
    bbox: list[float],
    start_date: str,
    end_date: str,
    destination_dir: Path,
    max_cloud_cover: float | None = None,
    asset_names: list[str] | None = None,
) -> dict:
    """Search, select and download a Sentinel-2 product."""

    if asset_names is None:
        asset_names = [
            "B02_10m",
            "B03_10m",
            "B04_10m",
            "B08_10m",
            "SCL_20m",
        ]

    items = search_sentinel2(
        bbox=bbox,
        start_date=start_date,
        end_date=end_date,
        max_cloud_cover=max_cloud_cover,
    )

    product = select_best_product(items)

    product_id = product["id"]
    product_dir = destination_dir / product_id

    downloaded_assets = {}

    for asset_name in asset_names:
        asset = get_asset(product, asset_name)

        local_path = download_asset(
            s3_client=s3_client,
            asset=asset,
            destination_dir=product_dir,
        )

        downloaded_assets[asset_name] = local_path

    return {
        "product": product,
        "product_id": product_id,
        "directory": product_dir,
        "assets": downloaded_assets,
    }