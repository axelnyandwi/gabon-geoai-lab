from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point, box


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "aoi"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


PLACES = {
    "libreville": (0.4086518, 9.4418849),
    "akanda": (0.5164243, 9.3882201),
    "owendo": (0.3208235, 9.4952738),
}

SIZE_KM = 12
HALF_SIZE_M = (SIZE_KM * 1000) / 2


for name, (lat, lon) in PLACES.items():

    # 1. Centre en coordonnées GPS
    center = gpd.GeoDataFrame(
        {"name": [name]},
        geometry=[Point(lon, lat)],
        crs="EPSG:4326",
    )

    # 2. Passage en UTM pour travailler en mètres
    center_utm = center.to_crs("EPSG:32632")

    x = center_utm.geometry.x.iloc[0]
    y = center_utm.geometry.y.iloc[0]

    # 3. Carré de 12 × 12 km
    geometry = box(
        x - HALF_SIZE_M,
        y - HALF_SIZE_M,
        x + HALF_SIZE_M,
        y + HALF_SIZE_M,
    )

    aoi = gpd.GeoDataFrame(
        {
            "name": [name],
            "type": ["acquisition"],
            "size_km": [SIZE_KM],
        },
        geometry=[geometry],
        crs="EPSG:32632",
    )

    # 4. Retour en WGS84
    aoi = aoi.to_crs("EPSG:4326")

    # 5. Sauvegarde GeoJSON
    output_path = OUTPUT_DIR / f"{name}.geojson"

    aoi.to_file(
        output_path,
        driver="GeoJSON",
    )

    print(f"{name} : {output_path}")
    print("Bounds :", aoi.total_bounds)