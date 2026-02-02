import math


def haversine_miles(lat1, lng1, lat2, lng2) -> float:
    """
    Distance between two lat/lng points in miles.
    """
    R = 3958.7613  # Earth radius in miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def cumulative_miles(coords):
    """
    coords: list of [lng, lat] from OSRM geojson geometry
    returns list cumulative distances aligned with coords indices
    """
    cum = [0.0]
    total = 0.0
    for i in range(1, len(coords)):
        lng1, lat1 = coords[i - 1]
        lng2, lat2 = coords[i]
        total += haversine_miles(lat1, lng1, lat2, lng2)
        cum.append(total)
    return cum
