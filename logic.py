import math, uuid, time, random

from data import STOPS, ROUTES, BUSES, USER_LOCATION

def move_buses():

    for route_id, bus in BUSES.items():

        stops = ROUTES[route_id]["stops"]

        total = len(stops)

        next_idx  = (bus["stop_idx"] + bus["direction"]) % total

        target    = STOPS[stops[next_idx]]

        tx, ty    = float(target["x"]), float(target["y"])

        dx   = tx - bus["x"]

        dy   = ty - bus["y"]

        dist = math.hypot(dx, dy)

        if dist < 4:

            bus["x"]        = tx

            bus["y"]        = ty

            bus["stop_idx"] = next_idx

            if next_idx == total - 1:

                bus["direction"] = -1

            elif next_idx == 0:

                bus["direction"] = 1

            bus["crowd"]      = random.choice(["Low", "Medium", "High"])

            bus["passengers"] = random.randint(5, 80)

        else:

            step    = 0.04

            bus["x"] += dx * step

            bus["y"] += dy * step

def get_etas(route_id):

    bus   = BUSES[route_id]

    stops = ROUTES[route_id]["stops"]

    results  = []

    cum_dist = 0.0

    for i, sid in enumerate(stops):

        s = STOPS[sid]

        if i == 0:

            cum_dist = math.hypot(s["x"] - bus["x"], s["y"] - bus["y"])

        else:

            prev = STOPS[stops[i - 1]]

            cum_dist += math.hypot(s["x"] - prev["x"], s["y"] - prev["y"])

        km      = cum_dist / 25

        minutes = (km / 18) * 60

        eta_str = "At stop" if minutes < 1 else f"{int(minutes)} min"

        results.append((s["name"], eta_str))

    return results

def nearest_stop():

    ux, uy    = USER_LOCATION["x"], USER_LOCATION["y"]

    best_id   = None

    best_dist = float("inf")

    for sid, s in STOPS.items():

        d = math.hypot(s["x"] - ux, s["y"] - uy)

        if d < best_dist:

            best_dist = d

            best_id   = sid

    s  = STOPS[best_id]

    km = best_dist / 25

    return s["name"], f"{km:.1f} km away"

def generate_ticket(from_id, to_id, route_id):

    fs   = STOPS[from_id]

    ts   = STOPS[to_id]

    dist = math.hypot(fs["x"] - ts["x"], fs["y"] - ts["y"])

    km   = max(dist / 25, 0.5)

    fare = int(km * 2.5 + 5)

    return {

        "id":    f"MH-{uuid.uuid4().hex[:8].upper()}",

        "route": ROUTES[route_id]["name"],

        "from":  fs["name"],

        "to":    ts["name"],

        "fare":  f"Rs. {fare}",

        "date":  time.strftime("%d %b %Y"),

        "time":  time.strftime("%H:%M"),

    }