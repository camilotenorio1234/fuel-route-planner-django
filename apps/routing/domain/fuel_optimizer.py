from dataclasses import dataclass
from typing import List, Dict, Any

from apps.fuels.loaders import Station
from apps.fuels.repositories import FuelRepo


@dataclass
class FuelStop:
    station_id: str
    name: str
    address: str
    city: str
    state: str
    lat: float
    lng: float
    price_per_gallon: float
    miles_from_start: float
    miles_since_last_stop: float
    gallons_to_buy: float
    cost: float


def plan_stops_by_state_segments(
    cum_miles: List[float],
    coords: List[List[float]],  # [lng, lat]
    repo: FuelRepo,
    geocoder,
    max_range_miles: float = 500.0,
    mpg: float = 10.0,
) -> Dict[str, Any]:
    total_distance = cum_miles[-1] if cum_miles else 0.0
    if total_distance == 0:
        return {"stops": [], "total_cost": 0.0}

    stops: List[FuelStop] = []
    total_cost = 0.0

    def idx_for_mile(target: float) -> int:
        lo, hi = 0, len(cum_miles) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if cum_miles[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    # puntos objetivo: 0, 500, 1000, ...
    last_mile = 0.0
    target = 0.0

    while target < total_distance:
        idx = idx_for_mile(target)
        lng, lat = coords[idx]

        # 1) estado del punto de ruta
        state = geocoder.reverse_state(lat, lng)
        if not state or len(state) != 2:
            raise ValueError(f"Could not resolve state code at mile {target:.1f}")

        # 2) estación más barata del estado
        st = repo.cheapest_in_state(state)
        if not st:
            raise ValueError(f"No stations found in state {state}")

        # 3) geocode de la estación
        full_addr = f"{st.address}, {st.city}, {st.state}, USA"
        loc = geocoder.geocode_address(full_addr)
        if not loc:
            raise ValueError(f"Could not geocode station address: {full_addr}")

        # 4) cuánto comprar para el siguiente tramo
        next_end = min(target + max_range_miles, total_distance)
        leg_miles = next_end - last_mile
        gallons = leg_miles / mpg
        cost = gallons * st.price_per_gallon
        total_cost += cost

        stops.append(
            FuelStop(
                station_id=st.station_id,
                name=st.name,
                address=st.address,
                city=st.city,
                state=st.state,
                lat=loc["lat"],
                lng=loc["lng"],
                price_per_gallon=st.price_per_gallon,
                miles_from_start=round(last_mile, 2),
                miles_since_last_stop=round(leg_miles, 2),
                gallons_to_buy=round(gallons, 2),
                cost=round(cost, 2),
            )
        )

        last_mile = next_end
        target += max_range_miles

    return {"stops": stops, "total_cost": round(total_cost, 2)}
