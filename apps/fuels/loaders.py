import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Station:
    station_id: str
    name: str
    address: str
    city: str
    state: str
    price_per_gallon: float


def load_stations_from_csv(csv_path: Path) -> List[Station]:
    if not csv_path.exists():
        raise FileNotFoundError(f"Fuel prices CSV not found at: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")

        required = ["OPIS Truckstop ID", "Truckstop Name", "Address", "City", "State", "Retail Price"]
        missing = [c for c in required if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"CSV missing columns: {missing}. Found: {reader.fieldnames}")

        stations: List[Station] = []
        for row in reader:
            try:
                price = float(row["Retail Price"])
            except Exception:
                continue

            stations.append(
                Station(
                    station_id=str(row["OPIS Truckstop ID"]).strip(),
                    name=str(row["Truckstop Name"]).strip(),
                    address=str(row["Address"]).strip(),
                    city=str(row["City"]).strip(),
                    state=str(row["State"]).strip(),
                    price_per_gallon=price,
                )
            )

        if not stations:
            raise ValueError("No stations loaded from CSV.")
        return stations
