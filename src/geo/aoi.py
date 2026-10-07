from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AOI_DIR = PROJECT_ROOT / "data" / "aoi"


def load_aoi(name: str) -> dict:
    """
    Charge une AOI GeoJSON depuis data/aoi/.

    Exemple :
        load_aoi("libreville")
        load_aoi("akanda")
        load_aoi("owendo")
    """

    aoi_path = AOI_DIR / f"{name.lower()}.geojson"

    if not aoi_path.exists():
        raise FileNotFoundError(
            f"AOI introuvable : {aoi_path}"
        )

    with open(aoi_path, "r", encoding="utf-8") as file:
        return json.load(file)