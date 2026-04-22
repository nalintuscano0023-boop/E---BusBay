import tkinter as tk

from tkinter import ttk

import time

from data import STOPS, ROUTES, BUSES, COLORS, USER_LOCATION

from logic import move_buses, get_etas, nearest_stop, generate_ticket

class SafarSathiApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("SafarSathi - Mumbai Bus Tracker")

        self.geometry("1100x720")

        self.resizable(True, True)

        self.configure(bg=COLORS["bg"])

        self.selected_route  = "BUS-01"

        self._route_keys     = []

        self._tick           = 0

        self._map_ready      = False

        self._crowd_widgets  = {}

        self._build_ui()

        self.after(100, self._init_static_map)

        self._loop()

    def _build_ui(self):

        self._build_header()

        body = tk.Frame(self, bg=COLORS["bg"])

        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._build_map_panel(body)

        self._build_sidebar(body)

    def _build_header(self):

        hdr = tk.Frame(self, bg=COLORS["panel"], height=58)

        hdr.pack(fill="x")

        hdr.pack_propagate(False)

        logo_c = tk.Canvas(hdr, width=52, height=44,

                           bg=COLORS["panel"], highlightthickness=0)

        logo_c.pack(side="left", padx=(12, 4), pady=6)

        self._draw_bus_logo(logo_c, 26, 22)

        name_frame = tk.Frame(hdr, bg=COLORS["panel"])

        name_frame.pack(side="left", pady=6)

        tk.Label(name_frame, text="SafarSathi",

                 font=("Helvetica", 17, "bold"),

                 bg=COLORS["panel"], fg=COLORS["accent"]).pack(anchor="w")

        tk.Label(name_frame, text="Mumbai Bus Tracker",

                 font=("Helvetica", 8),

                 bg=COLORS["panel"], fg=COLORS["muted"]).pack(anchor="w")

        self.clock_lbl = tk.Label(hdr, text="",

                                  font=("Helvetica", 11),

                                  bg=COLORS["panel"], fg=COLORS["muted"])

        self.clock_lbl.pack(side="right", padx=16)

    def _draw_bus_logo(self, c, cx, cy):

        W, H = 40, 22

        x1, y1 = cx - W//2, cy - H//2

        x2, y2 = cx + W//2, cy + H//2

        r = 4

        acc  = COLORS["accent"]

        dark = "#0d1117"

        wht  = "#e0e0e0"

        pts = [

            x1+r, y1,   x2-r, y1,

            x2,   y1,   x2,   y1+r,

            x2,   y2-r, x2,   y2,

            x2-r, y2,   x1+r, y2,

            x1,   y2,   x1,   y2-r,

            x1,   y1+r, x1,   y1,

        ]

        c.create_polygon(pts, smooth=True, fill=acc, outline="")

        c.create_rectangle(x1+r, y1+1, x2-r, y1+8, fill="#ffae55", outline="")

        for i in range(3):

            wx = x1 + 5 + i * 12

            c.create_rectangle(wx, y1+2, wx+8, y1+8,

                               fill=dark, outline=wht, width=1)

        c.create_rectangle(x2-10, y1+2, x2-2, y1+10,

                           fill="#6bcfff", outline=wht, width=1)

        for wx in [x1+7, x2-7]:

            c.create_oval(wx-5, y2-4, wx+5, y2+6,

                          fill=dark, outline=wht, width=1)

            c.create_oval(wx-2, y2-1, wx+2, y2+3,

                          fill="#555", outline="")

        c.create_oval(x2-4, y1+11, x2+1, y1+15,

                      fill="#ffe066", outline="")

        c.create_line(x1+16, y1+9, x1+16, y2, fill=dark, width=1)

    def _build_map_panel(self, parent):

        frame = tk.Frame(parent, bg=COLORS["panel"], bd=1, relief="solid")

        frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        tk.Label(frame, text="Live Map",

                 font=("Helvetica", 12, "bold"),

                 bg=COLORS["panel"], fg=COLORS["text"]).pack(anchor="w", padx=10, pady=(8, 2))

        self.canvas = tk.Canvas(frame, bg="#0d1117", highlightthickness=0)

        self.canvas.pack(fill="both", expand=True, padx=6, pady=(0, 4))

        self.near_lbl = tk.Label(frame, text="Nearest stop: —",

                                 font=("Helvetica", 9),

                                 bg=COLORS["panel"], fg=COLORS["muted"])

        self.near_lbl.pack(pady=(0, 6))

    def _init_static_map(self):

        c = self.canvas

        for rid, route in ROUTES.items():

            stops = route["stops"]

            for i in range(len(stops) - 1):

                s1 = STOPS[stops[i]]

                s2 = STOPS[stops[i + 1]]

                c.create_line(s1["x"], s1["y"], s2["x"], s2["y"],

                               fill=route["color"], width=2, dash=(8, 5),

                               tags="static")

        for sid, s in STOPS.items():

            x, y = s["x"], s["y"]

            c.create_oval(x-7, y-7, x+7, y+7,

                          fill="#0d1117", outline="#4488cc", width=2,

                          tags="static")

            c.create_text(x, y - 16, text=s["name"],

                          font=("Helvetica", 8), fill=COLORS["muted"],

                          tags="static")

        ux, uy = USER_LOCATION["x"], USER_LOCATION["y"]

        c.create_oval(ux-7, uy-7, ux+7, uy+7,

                      fill=COLORS["accent"], outline="white", width=1,

                      tags="static")

        c.create_text(ux, uy + 16, text="You",

                      font=("Helvetica", 8, "bold"), fill=COLORS["accent"],

                      tags="static")

        for rid, bus in BUSES.items():

            col = ROUTES[rid]["color"]

            bx, by = bus["x"], bus["y"]

            c.create_oval(bx-10, by-10, bx+10, by+10,

                          fill=col, outline="white", width=1,

                          tags=(f"oval_{rid}", "bus"))

            c.create_text(bx, by, text="B",

                          font=("Helvetica", 8, "bold"), fill="white",

                          tags=(f"btxt_{rid}", "bus"))

            c.create_text(bx, by + 20, text=rid,

                          font=("Helvetica", 8), fill=col,

                          tags=(f"blbl_{rid}", "bus"))

        self._map_ready = True

    def _update_buses_on_canvas(self):

        if not self._map_ready:

            return

        c = self.canvas

        for rid, bus in BUSES.items():

            bx, by = bus["x"], bus["y"]

            c.coords(f"oval_{rid}", bx-10, by-10, bx+10, by+10)

            c.coords(f"btxt_{rid}", bx, by)

            c.coords(f"blbl_{rid}", bx, by + 20)

    def _build_sidebar(self, parent):

        sb = tk.Frame(parent, bg=COLORS["bg"], width=330)

        sb.pack(side="right", fill="y")

        sb.pack_propagate(False)

        self._build_search(sb)

        self._build_eta(sb)

        self._build_crowd(sb)

        self._build_ticket(sb)

    def _build_search(self, parent):

        frame = tk.LabelFrame(parent, text="  Route Search  ",

                               bg=COLORS["panel"], fg=COLORS["accent"],

                               font=("Helvetica", 10, "bold"), bd=1)

        frame.pack(fill="x", pady=(0, 6))

        row = tk.Frame(frame, bg=COLORS["panel"])

        row.pack(fill="x", padx=8, pady=6)

        self.search_var = tk.StringVar()

        entry = tk.Entry(row, textvariable=self.search_var,

                         font=("Helvetica", 10),

                         bg=COLORS["bg"], fg=COLORS["text"],

                         insertbackground="white", relief="flat", bd=4)

        entry.pack(side="left", fill="x", expand=True)

        tk.Button(row, text="Go", bg=COLORS["accent"], fg="white",

                   font=("Helvetica", 9, "bold"), relief="flat", padx=10,

                   cursor="hand2", command=self._do_search).pack(side="left", padx=(4, 0))

        entry.bind("<Return>", lambda e: self._do_search())

        self.route_list = tk.Listbox(frame, height=4,

                                      bg=COLORS["bg"], fg=COLORS["text"],

                                      selectbackground=COLORS["accent"],

                                      selectforeground="white",

                                      font=("Helvetica", 9), relief="flat",

                                      activestyle="none", cursor="hand2")

        self.route_list.pack(fill="x", padx=8, pady=(0, 8))

        self.route_list.bind("<<ListboxSelect>>", self._on_route_select)

        self._load_all_routes()

    def _load_all_routes(self):

        self.route_list.delete(0, "end")

        self._route_keys = list(ROUTES.keys())

        for rid in self._route_keys:

            self.route_list.insert("end", f"  {rid}  —  {ROUTES[rid]['name']}")

    def _do_search(self):

        q = self.search_var.get().strip().upper()

        if not q:

            self._load_all_routes()

            return

        self.route_list.delete(0, "end")

        self._route_keys = []

        for rid, r in ROUTES.items():

            if q in rid or q in r["name"].upper():

                self._route_keys.append(rid)

                self.route_list.insert("end", f"  {rid}  —  {r['name']}")

        if not self._route_keys:

            self.route_list.insert("end", "  No results found")

    def _on_route_select(self, event):

        sel = self.route_list.curselection()

        if sel and sel[0] < len(self._route_keys):

            self.selected_route = self._route_keys[sel[0]]

            self._refresh_eta()

    def _build_eta(self, parent):

        frame = tk.LabelFrame(parent, text="  ETA by Stop  ",

                               bg=COLORS["panel"], fg=COLORS["accent"],

                               font=("Helvetica", 10, "bold"), bd=1)

        frame.pack(fill="x", pady=(0, 6))

        self.eta_list = tk.Listbox(frame, height=5,

                                    bg=COLORS["bg"], fg=COLORS["text"],

                                    font=("Courier", 9), relief="flat",

                                    activestyle="none",

                                    selectbackground=COLORS["bg"])

        self.eta_list.pack(fill="x", padx=8, pady=8)

    def _refresh_eta(self):

        self.eta_list.delete(0, "end")

        for sname, eta in get_etas(self.selected_route):

            self.eta_list.insert("end", f"  {sname:<16}  {eta:>8}")

        if self.eta_list.size() > 0:

            self.eta_list.itemconfig(0, fg=COLORS["accent"])

    def _build_crowd(self, parent):

        frame = tk.LabelFrame(parent, text="  Crowd Level  ",

                               bg=COLORS["panel"], fg=COLORS["accent"],

                               font=("Helvetica", 10, "bold"), bd=1)

        frame.pack(fill="x", pady=(0, 6))

        self._crowd_widgets = {}

        for rid in ROUTES:

            row = tk.Frame(frame, bg=COLORS["bg"])

            row.pack(fill="x", padx=8, pady=3)

            tk.Label(row, text=f"  {rid}", font=("Helvetica", 9, "bold"),

                      width=9, anchor="w",

                      bg=COLORS["bg"], fg=ROUTES[rid]["color"]).pack(side="left")

            crowd_lbl = tk.Label(row, text="—", font=("Helvetica", 9),

                                  width=10, anchor="w",

                                  bg=COLORS["bg"], fg=COLORS["text"])

            crowd_lbl.pack(side="left")

            pax_lbl = tk.Label(row, text="—", font=("Helvetica", 8),

                                bg=COLORS["bg"], fg=COLORS["muted"])

            pax_lbl.pack(side="left", padx=4)

            self._crowd_widgets[rid] = (crowd_lbl, pax_lbl)

        tk.Frame(frame, bg=COLORS["panel"], height=4).pack()

    def _refresh_crowd(self):

        clr_map = {

            "Low":    COLORS["green"],

            "Medium": COLORS["yellow"],

            "High":   COLORS["red"],

        }

        for rid, bus in BUSES.items():

            if rid not in self._crowd_widgets:

                continue

            crowd_lbl, pax_lbl = self._crowd_widgets[rid]

            level = bus["crowd"]

            crowd_lbl.config(text=level, fg=clr_map.get(level, COLORS["text"]))

            pax_lbl.config(text=f"{bus['passengers']} pax")

    def _build_ticket(self, parent):

        frame = tk.LabelFrame(parent, text="  Ticket Generator  ",

                               bg=COLORS["panel"], fg=COLORS["accent"],

                               font=("Helvetica", 10, "bold"), bd=1)

        frame.pack(fill="x")

        stop_names     = [f"{sid} – {s['name']}" for sid, s in STOPS.items()]

        self._stop_ids = list(STOPS.keys())

        r1 = tk.Frame(frame, bg=COLORS["panel"])

        r1.pack(fill="x", padx=8, pady=(8, 3))

        tk.Label(r1, text="From:", font=("Helvetica", 9),

                  bg=COLORS["panel"], fg=COLORS["muted"]).pack(side="left")

        self.from_cb = ttk.Combobox(r1, values=stop_names, width=17,

                                     state="readonly", font=("Helvetica", 9))

        self.from_cb.pack(side="left", padx=4)

        r2 = tk.Frame(frame, bg=COLORS["panel"])

        r2.pack(fill="x", padx=8, pady=(0, 6))

        tk.Label(r2, text="To:  ", font=("Helvetica", 9),

                  bg=COLORS["panel"], fg=COLORS["muted"]).pack(side="left")

        self.to_cb = ttk.Combobox(r2, values=stop_names, width=17,

                                   state="readonly", font=("Helvetica", 9))

        self.to_cb.pack(side="left", padx=4)

        tk.Button(frame, text="Generate Ticket",

                   bg=COLORS["green"], fg="white",

                   font=("Helvetica", 9, "bold"), relief="flat",

                   padx=10, pady=4, cursor="hand2",

                   command=self._gen_ticket).pack(pady=(0, 6))

        self.ticket_lbl = tk.Label(frame,

                                    text="  Select From and To stops, then click Generate.",

                                    font=("Helvetica", 9, "italic"),

                                    bg=COLORS["bg"], fg=COLORS["muted"],

                                    justify="left", anchor="w",

                                    pady=8, padx=10)

        self.ticket_lbl.pack(fill="x", padx=8, pady=(0, 8))

    def _gen_ticket(self):

        fi = self.from_cb.current()

        ti = self.to_cb.current()

        if fi == -1 or ti == -1:

            self.ticket_lbl.config(

                text="  [!]  Please select both From and To stops.",

                font=("Helvetica", 9, "italic"),

                fg=COLORS["yellow"])

            return

        if fi == ti:

            self.ticket_lbl.config(

                text="  [!]  From and To stops must be different!",

                font=("Helvetica", 9, "italic"),

                fg=COLORS["red"])

            return

        t = generate_ticket(self._stop_ids[fi], self._stop_ids[ti],

                             self.selected_route)

        self.ticket_lbl.config(

            font=("Courier", 9),

            fg=COLORS["text"],

            text=(

                f"  ID    : {t['id']}\n"

                f"  Route : {t['route']}\n"

                f"  From  : {t['from']}\n"

                f"  To    : {t['to']}\n"

                f"  Fare  : {t['fare']}   {t['date']}  {t['time']}"

            )

        )

    def _loop(self):

        self._tick += 1

        self.clock_lbl.config(text=time.strftime("%H:%M:%S"))

        move_buses()

        self._update_buses_on_canvas()

        self._refresh_crowd()

        if self._tick % 10 == 0:

            self._refresh_eta()

        if self._tick % 15 == 0:

            name, dist = nearest_stop()

            self.near_lbl.config(text=f"Nearest stop: {name}  ({dist})")

        self.after(200, self._loop)