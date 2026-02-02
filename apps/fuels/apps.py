from django.apps import AppConfig
from pathlib import Path
from apps.fuels.loaders import load_stations_from_csv
from apps.fuels.repositories import FuelRepo


class FuelsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.fuels"

    repo: FuelRepo | None = None

    def ready(self):
        base_dir = Path(__file__).resolve().parent.parent.parent  # raíz del proyecto
        csv_path = base_dir / "data" / "fuel-prices-for-be-assessment.csv"

        stations = load_stations_from_csv(csv_path)
        self.__class__.repo = FuelRepo.build(stations)
