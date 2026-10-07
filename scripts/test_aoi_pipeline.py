from pathlib import Path

import geopandas as gpd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AOI_DIR = PROJECT_ROOT / "data" / "aoi"


AOIS = [
    "libreville",
    "akanda",
    "owendo",
]


for name in AOIS:

    print(f"\n--- {name.upper()} ---")

    path = AOI_DIR / f"{name}.geojson"

    gdf = gpd.read_file(path)

    print("Fichier :", path)
    print("CRS :", gdf.crs)
    print("Type :", gdf.geometry.iloc[0].geom_type)
    print("Valide :", gdf.geometry.iloc[0].is_valid)
    print("Bounds :", gdf.total_bounds)

    # Projection dans le CRS Sentinel-2 de notre produit actuel
    gdf_s2 = gdf.to_crs("EPSG:32632")

    print("Bounds UTM 32N :", gdf_s2.total_bounds)