from pathlib import Path

from src.data.quality import calculate_scl_quality


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCL_PATH = (
    PROJECT_ROOT
    / "data"
    / "interim"
    / "sentinel2"
    / "ndvi_test"
    / "libreville"
    / "libreville_SCL_20m.tif"
)


quality = calculate_scl_quality(SCL_PATH)


print("Qualité SCL - Libreville")
print("------------------------")

for key, value in quality.items():

    if isinstance(value, float):
        print(f"{key} : {value:.2f}")
    else:
        print(f"{key} : {value}")