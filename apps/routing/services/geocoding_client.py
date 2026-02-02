import json
import time
from pathlib import Path
import requests

NOMINATIM_BASE = "https://nominatim.openstreetmap.org"
EMAIL = "juanca1926@gmail.com"  # <-- pon un correo válido
USER_AGENT = f"fuel-route-planner-assignment/1.0 ({EMAIL})"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
}
US_STATE_TO_ABBR = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY",
}

class Geocoder:
    def __init__(self, cache_path: Path):
        self.cache_path = cache_path
        self.cache = self._load_cache()

    def _load_cache(self):
        if self.cache_path.exists():
            try:
                return json.loads(self.cache_path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        self.cache_path.write_text(json.dumps(self.cache, indent=2), encoding="utf-8")

    def geocode_address(self, address: str) -> dict | None:
        key = f"addr::{address}".strip().lower()
        if key in self.cache:
            return self.cache[key]

        url = f"{NOMINATIM_BASE}/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1,
            "countrycodes": "us",
            "email": EMAIL,
        }

        time.sleep(1.0)
        r = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if r.status_code == 403:
            return None
        r.raise_for_status()

        arr = r.json()
        if not arr:
            return None

        hit = arr[0]
        result = {"lat": float(hit["lat"]), "lng": float(hit["lon"])}

        self.cache[key] = result
        self._save_cache()
        return result

    


    def reverse_state(self, lat: float, lng: float) -> str | None:
        key = f"rev::{lat:.5f},{lng:.5f}"
        if key in self.cache:
            # si quedó cacheado None, lo vas a seguir viendo
            return self.cache[key].get("state")

        url = f"{NOMINATIM_BASE}/reverse"
        params = {
            "lat": lat,
            "lon": lng,
            "format": "jsonv2",
            "addressdetails": 1,
            "zoom": 5,   # nivel estado
            "email": EMAIL,
        }
        time.sleep(1.0)
        r = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if r.status_code == 403:
            self.cache[key] = {"state": None}
            self._save_cache()
            return None
        r.raise_for_status()

        data = r.json()
        addr = data.get("address", {}) or {}

        state_code = None

        # 1) Mejor caso: ISO3166-2 (ej: "US-NY")
        iso = addr.get("ISO3166-2-lvl4") or addr.get("ISO3166-2-lvl6")
        if isinstance(iso, str) and iso.startswith("US-") and len(iso) == 5:
            state_code = iso.split("-")[1].upper()

        # 2) Segundo caso: a veces viene state_code (no siempre)
        if not state_code:
            sc = addr.get("state_code")
            if isinstance(sc, str) and len(sc.strip()) == 2:
                state_code = sc.strip().upper()

        # 3) Caso común: viene "state": "New York"
        if not state_code:
            st_name = addr.get("state")
            if isinstance(st_name, str):
                state_code = US_STATE_TO_ABBR.get(st_name.strip().lower())

        # Normaliza
        if state_code and len(state_code) != 2:
            state_code = None

        self.cache[key] = {"state": state_code}
        self._save_cache()
        return state_code
