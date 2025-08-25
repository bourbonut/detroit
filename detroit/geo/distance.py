from .length import geo_length

def geo_distance(a: float, b: float) -> float:
    return geo_length({"type": "LineString", "coordinates": [a, b]})
