STOPS = {

    "S01": {"name": "Dadar",   "x": 80,  "y": 300},

    "S02": {"name": "Bandra",  "x": 230, "y": 200},

    "S03": {"name": "Andheri", "x": 350, "y": 130},

    "S04": {"name": "Malad",   "x": 510, "y": 120},

    "S05": {"name": "Borivali","x": 570, "y": 100},

    "S06": {"name": "CST",     "x": 60,  "y": 410},

    "S07": {"name": "Worli",   "x": 160, "y": 390},

    "S08": {"name": "Kurla",   "x": 220, "y": 360},

    "S09": {"name": "Thane",   "x": 560, "y": 260},

}

ROUTES = {

    "BUS-01": {

        "name":  "Borivali to Dadar",

        "stops": ["S05", "S04", "S03", "S02", "S01"],

        "color": "orange",

    },

    "BUS-09": {

        "name":  "CST to Bandra",

        "stops": ["S06", "S07", "S01", "S02"],

        "color": "blue",

    },

    "BUS-27": {

        "name":  "Dadar to Thane",

        "stops": ["S01", "S08", "S09"],

        "color": "green",

    },

}

BUSES = {

    "BUS-01": {"stop_idx": 0, "x": 570.0, "y": 100.0, "direction": 1, "crowd": "Low",    "passengers": 10},

    "BUS-09": {"stop_idx": 0, "x": 60.0,  "y": 410.0, "direction": 1, "crowd": "High",   "passengers": 70},

    "BUS-27": {"stop_idx": 0, "x": 80.0,  "y": 300.0, "direction": 1, "crowd": "Medium", "passengers": 40},

}

USER_LOCATION = {"x": 250, "y": 300}

COLORS = {

    "bg":      "#1e1e2e",

    "panel":   "#2a2a3e",

    "text":    "#ffffff",

    "muted":   "#888888",

    "accent":  "#f78c1e",

    "green":   "#2ea043",

    "yellow":  "#f0b429",

    "red":     "#e84855",

    "border":  "#444466",

}