import pytest
from src.data.ingestion import get_asset, get_s3_key
from src.data.ingestion import get_s3_key
from unittest.mock import Mock
from src.data.ingestion import download_asset, get_asset, get_s3_key


def test_get_s3_key():
    asset = {
        "href": "s3://eodata/Sentinel-2/test/B04_10m.jp2"
    }

    result = get_s3_key(asset)

    assert result == "Sentinel-2/test/B04_10m.jp2"

def test_get_s3_key_rejects_wrong_bucket():
    asset = {
        "href": "s3://wrong-bucket/Sentinel-2/test/B04_10m.jp2"
    }

    with pytest.raises(ValueError):
        get_s3_key(asset)

def test_get_asset():
    item = {
        "assets": {
            "B04_10m": {
                "href": "s3://eodata/Sentinel-2/test/B04_10m.jp2"
            }
        }
    }

    result = get_asset(item, "B04_10m")

    assert result["href"] == "s3://eodata/Sentinel-2/test/B04_10m.jp2"


def test_get_asset_rejects_missing_asset():
    item = {
        "assets": {}
    }

    with pytest.raises(ValueError):
        get_asset(item, "B08_10m")

def test_download_asset(tmp_path):
    s3_client = Mock()

    asset = {
        "href": "s3://eodata/Sentinel-2/test/B04_10m.jp2"
    }

    result = download_asset(
        s3_client=s3_client,
        asset=asset,
        destination_dir=tmp_path,
    )

    expected_path = tmp_path / "B04_10m.jp2"

    assert result == expected_path

    s3_client.download_file.assert_called_once_with(
        "eodata",
        "Sentinel-2/test/B04_10m.jp2",
        str(expected_path),
    )

def test_download_asset_uses_cache(tmp_path):
    s3_client = Mock()

    asset = {
        "href": "s3://eodata/Sentinel-2/test/B04_10m.jp2"
    }

    cached_file = tmp_path / "B04_10m.jp2"
    cached_file.touch()

    result = download_asset(
        s3_client=s3_client,
        asset=asset,
        destination_dir=tmp_path,
    )

    assert result == cached_file
    s3_client.download_file.assert_not_called()