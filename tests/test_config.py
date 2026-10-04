"""Vérification des chemins de configuration, sans accès réseau ni données réelles."""

import importlib

from src import config


def test_data_paths(monkeypatch):
    """Vérifie les valeurs par défaut et les chemins configurables."""
    original = config
    try:
        monkeypatch.delenv("GABON_GEOAI_DATA_DIR", raising=False)
        settings = importlib.reload(config)
        assert settings.DATA_DIR == settings.PROJECT_ROOT / "data"
        assert settings.RAW_DATA_DIR == settings.DATA_DIR / "raw"
        assert settings.INTERIM_DATA_DIR == settings.DATA_DIR / "interim"
        assert settings.PROCESSED_DATA_DIR == settings.DATA_DIR / "processed"

        monkeypatch.setenv("GABON_GEOAI_DATA_DIR", "custom_data")
        settings = importlib.reload(config)
        assert settings.DATA_DIR == settings.PROJECT_ROOT / "custom_data"

        absolute_path = (settings.PROJECT_ROOT.parent / "external_data").resolve()
        monkeypatch.setenv("GABON_GEOAI_DATA_DIR", str(absolute_path))
        assert importlib.reload(config).DATA_DIR == absolute_path

        monkeypatch.setenv("GABON_GEOAI_DATA_DIR", "   ")
        assert importlib.reload(config).DATA_DIR == settings.PROJECT_ROOT / "data"
    finally:
        monkeypatch.undo()
        importlib.reload(original)
