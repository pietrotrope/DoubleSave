import math

def coords_distance(lat1, lon1, lat2, lon2):

    R = 6371e3  # meters
    φ1 = lat1 * math.pi / 180  # φ, λ in radians
    φ2 = lat2 * math.pi / 180
    Δφ = (lat2 - lat1) * math.pi / 180
    Δλ = (lon2 - lon1) * math.pi / 180

    a = math.sin(Δφ / 2) * math.sin(Δφ / 2) + \
        math.cos(φ1) * math.cos(φ2) * \
        math.sin(Δλ / 2) * math.sin(Δλ / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c  # in meters

    return d

def stores_in_radius(coords, stores, radius=2):
    radius_m = radius*1000
    close_stores = []
    for store in stores:
        dist = coords_distance(coords[0], coords[1], store[1][0], store[1][1])
        if dist <= radius_m:
            close_stores.append((store[0], dist/1000, store[1]))
    return close_stores