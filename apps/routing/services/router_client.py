import requests


OSRM_BASE_URL = "https://router.project-osrm.org"


class OSRMClient:
    @staticmethod
    def get_route(start_lat, start_lng, end_lat, end_lng):
        """
        Returns:
            {
              distance_miles,
              duration_minutes,
              geometry (GeoJSON LineString)
            }
        """
        url = (
            f"{OSRM_BASE_URL}/route/v1/driving/"
            f"{start_lng},{start_lat};{end_lng},{end_lat}"
        )

        params = {
            "overview": "full",
            "geometries": "geojson",
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        route = data["routes"][0]

        distance_miles = route["distance"] / 1609.34
        duration_minutes = route["duration"] / 60

        return {
            "distance_miles": round(distance_miles, 2),
            "duration_minutes": round(duration_minutes, 1),
            "geometry": route["geometry"],
        }
