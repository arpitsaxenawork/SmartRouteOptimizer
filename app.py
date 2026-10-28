"""
Smart Route Optimization Using Graph Algorithms | DAA MCA Mini Project
Chandigarh University (CU) Campus Network Simulation
Features: Adjacency List/Matrix, Dijkstra, BFS, DFS, Kruskal, Prim, Tkinter GUI
"""
import sys, time, heapq, tkinter as tk
from tkinter import ttk, scrolledtext
from collections import deque
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx

# --- 1. CAMPUS GRAPH DATA (15 LOCATIONS, 25 WEIGHTED EDGES) ---
LOCATIONS = {
    0: "Main Gate (NH-05)", 1: "Admin Block", 2: "Block A1 (Engg 1)",
    3: "Block A2 (Engg 2)", 4: "Block B1 (UIC-MCA)", 5: "Block C1 (USB)",
    6: "Central Library", 7: "Student Center", 8: "Innovation Park",
    9: "Auditorium", 10: "Sports Complex", 11: "North Boys Hostel",
    12: "South Girls Hostel", 13: "Medical Centre", 14: "Transport Terminal"
}

COORDS = {
    0: (1.0, 2.5), 14: (1.8, 1.2), 1: (3.2, 3.2), 2: (4.8, 4.8), 3: (6.6, 4.5),
    4: (7.4, 3.2), 5: (6.0, 2.2), 6: (4.4, 2.8), 7: (4.5, 1.5), 8: (6.2, 1.1),
    9: (2.8, 2.0), 10: (2.8, 0.4), 11: (8.4, 2.2), 12: (7.8, 0.8), 13: (1.6, 0.2)
}

EDGES = [
    (0, 1, 200), (0, 14, 150), (14, 1, 180), (1, 2, 220), (1, 6, 210), (1, 9, 250),
    (2, 3, 190), (2, 6, 260), (3, 4, 210), (4, 5, 230), (4, 11, 280), (5, 6, 240),
    (5, 7, 180), (5, 8, 220), (6, 7, 190), (6, 9, 170), (7, 8, 200), (7, 10, 270),
    (8, 11, 290), (8, 12, 230), (9, 10, 240), (9, 13, 160), (10, 13, 210),
    (11, 12, 220), (14, 13, 260)
]

# ==============================================================================
# 2. GRAPH REPRESENTATIONS: ADJACENCY LIST & ADJACENCY MATRIX
# ==============================================================================

class CampusGraph:
    """Maintains dual representations demonstrating O(V+E) vs O(V^2) trade-offs."""
    def __init__(self, locations, edges):
        self.n = len(locations)
        self.locations = locations
        self.edges = edges
        self.adj_list = {i: [] for i in range(self.n)}
        self.adj_matrix = [[0 if i == j else float('inf') for j in range(self.n)] for i in range(self.n)]

        for u, v, w in edges:
            self.adj_list[u].append((v, w))
            self.adj_list[v].append((u, w))
            self.adj_matrix[u][v] = w
            self.adj_matrix[v][u] = w

# ==============================================================================
# 3. DISJOINT SET UNION (UNION BY RANK & PATH COMPRESSION)
# ==============================================================================

class DSU:
    """Disjoint Set Union with O(alpha(V)) amortized time complexity."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.ops = 0

    def find(self, i):
        self.ops += 1
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Path compression
        return self.parent[i]

    def union(self, root_x, root_y):
        self.ops += 1
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

# ==============================================================================
# 4. ALGORITHM ENGINE IMPLEMENTED FROM FIRST PRINCIPLES
# ==============================================================================

class RouteEngine:
    """Core algorithmic solver tracking elementary operations and execution times."""
    def __init__(self, graph):
        self.g = graph

    def dijkstra(self, src, dest):
        """Single-Source Shortest Path using Greedy Min-Heap Priority Queue."""
        t0 = time.perf_counter()
        dist = {i: float('inf') for i in range(self.g.n)}
        pred = {i: None for i in range(self.g.n)}
        dist[src], ops, visited = 0, 1, set()
        pq = [(0, src)]

        while pq:
            d, u = heapq.heappop(pq)
            ops += 1
            if u in visited:
                continue
            visited.add(u)
            if u == dest:
                break

            for v, w in self.g.adj_list[u]:
                ops += 1
                if v not in visited and d + w < dist[v]:
                    dist[v] = d + w
                    pred[v] = u
                    heapq.heappush(pq, (dist[v], v))
                    ops += 1

        path, curr = [], dest
        if dist[dest] != float('inf'):
            while curr is not None:
                path.append(curr)
                curr = pred[curr]
            path.reverse()

        elapsed = (time.perf_counter() - t0) * 1e6
        return {"algo": "Dijkstra", "path": path, "dist": dist[dest], "hops": max(0, len(path)-1),
                "ops": ops, "time_us": round(elapsed, 2), "tc": "O((V+E) log V)", "sc": "O(V)"}

    def bfs(self, src, dest):
        """Breadth-First Search finding path with minimum hops/turns."""
        t0 = time.perf_counter()
        q, visited, pred, ops = deque([src]), {src}, {src: None}, 1
        found = False

        while q:
            u = q.popleft()
            ops += 1
            if u == dest:
                found = True
                break
            for v, _ in self.g.adj_list[u]:
                ops += 1
                if v not in visited:
                    visited.add(v)
                    pred[v] = u
                    q.append(v)
                    ops += 1

        path, d = [], 0
        if found:
            curr = dest
            while curr is not None:
                path.append(curr)
                curr = pred[curr]
            path.reverse()
            d = sum(self.g.adj_matrix[path[i]][path[i+1]] for i in range(len(path)-1))

        elapsed = (time.perf_counter() - t0) * 1e6
        return {"algo": "BFS", "path": path, "dist": d if found else None, "hops": max(0, len(path)-1),
                "ops": ops, "time_us": round(elapsed, 2), "tc": "O(V + E)", "sc": "O(V)"}

    def dfs(self, src, dest):
        """Depth-First Search demonstrating unweighted exploratory traversal."""
        t0 = time.perf_counter()
        visited, path, ops = set(), [], 0

        def traverse(u):
            nonlocal ops
            ops += 1
            visited.add(u)
            path.append(u)
            if u == dest:
                return True
            for v, _ in self.g.adj_list[u]:
                ops += 1
                if v not in visited and traverse(v):
                    return True
            path.pop()
            return False

        traverse(src)
        d = sum(self.g.adj_matrix[path[i]][path[i+1]] for i in range(len(path)-1)) if path else None
        elapsed = (time.perf_counter() - t0) * 1e6
        return {"algo": "DFS", "path": path, "dist": d, "hops": max(0, len(path)-1),
                "ops": ops, "time_us": round(elapsed, 2), "tc": "O(V + E)", "sc": "O(V)"}

    def kruskal(self):
        """Kruskal's Algorithm for Minimum Spanning Tree via Sorted Edges & DSU."""
        t0 = time.perf_counter()
        edges = sorted([(w, min(u, v), max(u, v)) for u, v, w in self.g.edges])
        dsu = DSU(self.g.n)
        mst, cost, ops = [], 0, len(edges)

        for w, u, v in edges:
            ops += 1
            ru, rv = dsu.find(u), dsu.find(v)
            if ru != rv:
                dsu.union(ru, rv)
                mst.append((u, v, w))
                cost += w
                if len(mst) == self.g.n - 1:
                    break

        elapsed = (time.perf_counter() - t0) * 1e6
        return {"algo": "Kruskal MST", "mst": mst, "cost": cost, "edges": len(mst),
                "ops": ops + dsu.ops, "time_us": round(elapsed, 2), "tc": "O(E log E)", "sc": "O(V+E)"}

    def prim(self, root=0):
        """Prim's Algorithm for Minimum Spanning Tree via Greedy Cut Expansion."""
        t0 = time.perf_counter()
        visited, mst, cost, ops = {root}, [], 0, 0
        pq = [(w, root, v) for v, w in self.g.adj_list[root]]
        heapq.heapify(pq)
        ops += len(pq)

        while pq and len(visited) < self.g.n:
            w, u, v = heapq.heappop(pq)
            ops += 1
            if v in visited:
                continue
            visited.add(v)
            mst.append((u, v, w))
            cost += w
            for nxt, nw in self.g.adj_list[v]:
                ops += 1
                if nxt not in visited:
                    heapq.heappush(pq, (nw, v, nxt))
                    ops += 1

        elapsed = (time.perf_counter() - t0) * 1e6
        return {"algo": "Prim MST", "mst": mst, "cost": cost, "edges": len(mst),
                "ops": ops, "time_us": round(elapsed, 2), "tc": "O((V+E) log V)", "sc": "O(V+E)"}

# ==============================================================================
# 5. GRAPHICAL USER INTERFACE (TKINTER + EMBEDDED MATPLOTLIB)
# ==============================================================================

class App:
    """Main Tkinter Dashboard for interactive graph route visualization."""
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Route Optimization | DAA Mini Project")
        self.root.geometry("1300x820")
        self.graph = CampusGraph(LOCATIONS, EDGES)
        self.engine = RouteEngine(self.graph)

        self.nx_g = nx.Graph()
        for u, name in LOCATIONS.items():
            self.nx_g.add_node(u, name=name)
        for u, v, w in EDGES:
            self.nx_g.add_edge(u, v, weight=w)

        self._build_ui()
        self.draw_graph()

    def _build_ui(self):
        # Header Bar
        hdr = tk.Frame(self.root, bg="#1A237E", padx=16, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="Smart Route Optimization Using Graph Algorithms",
                 font=("Segoe UI", 14, "bold"), fg="white", bg="#1A237E").pack(anchor="w")
        tk.Label(hdr, text="Chandigarh University (CU) Map | MCA 1st Sem DAA | Dijkstra, BFS, DFS, Kruskal, Prim",
                 font=("Segoe UI", 9), fg="#C5CAE9", bg="#1A237E").pack(anchor="w")

        # Layout Container
        main = ttk.Frame(self.root, padding=8)
        main.pack(fill=tk.BOTH, expand=True)

        # Controls & Metrics (Left Panel)
        left = ttk.Frame(main, width=420)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left.pack_propagate(False)

        locs = [f"{i}: {LOCATIONS[i]}" for i in range(len(LOCATIONS))]
        ttk.Label(left, text="Starting Location (Source):", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(2, 2))
        self.src_cb = ttk.Combobox(left, values=locs, state="readonly")
        self.src_cb.set(locs[0])
        self.src_cb.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(left, text="Destination Location (Target):", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(2, 2))
        self.dest_cb = ttk.Combobox(left, values=locs, state="readonly")
        self.dest_cb.set(locs[4])
        self.dest_cb.pack(fill=tk.X, pady=(0, 6))

        self.algos = ["Dijkstra's Shortest Path", "Breadth-First Search (BFS)", "Depth-First Search (DFS)",
                      "Kruskal's MST", "Prim's MST", "Compare All Algorithms"]
        ttk.Label(left, text="Algorithm Choice:", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(2, 2))
        self.algo_cb = ttk.Combobox(left, values=self.algos, state="readonly")
        self.algo_cb.set(self.algos[0])
        self.algo_cb.pack(fill=tk.X, pady=(0, 8))

        # Action Buttons
        bf = ttk.Frame(left)
        bf.pack(fill=tk.X, pady=(0, 8))
        ttk.Button(bf, text="▶ Run Algorithm", command=self.run_algo).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        ttk.Button(bf, text="↺ Reset", command=self.draw_graph).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))

        # Metrics Panel
        mf = ttk.LabelFrame(left, text=" Performance Metrics ", padding=8)
        mf.pack(fill=tk.X, pady=(0, 8))
        self.labels = {}
        for idx, (k, txt) in enumerate([("d", "Distance / Cost:"), ("h", "Hops / Edges:"),
                                        ("t", "Execution Time:"), ("o", "Operations:"),
                                        ("tc", "Time Complexity:"), ("sc", "Space Complexity:")]):
            ttk.Label(mf, text=txt, font=("Segoe UI", 8)).grid(row=idx, column=0, sticky="w", pady=1)
            self.labels[k] = ttk.Label(mf, text="--", font=("Segoe UI", 8, "bold"), foreground="#0D47A1")
            self.labels[k].grid(row=idx, column=1, sticky="e", pady=1)
        mf.columnconfigure(0, weight=1)
        mf.columnconfigure(1, weight=1)

        # Execution Log
        ttk.Label(left, text="Execution Trace & Route Output:", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.log = scrolledtext.ScrolledText(left, wrap=tk.WORD, font=("Consolas", 8), bg="#F8F9FA", height=12)
        self.log.pack(fill=tk.BOTH, expand=True)

        # Canvas (Right Panel)
        right = ttk.Frame(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tb = NavigationToolbar2Tk(self.canvas, right)
        tb.update()

    def get_nodes(self):
        return int(self.src_cb.get().split(":")[0]), int(self.dest_cb.get().split(":")[0])

    def draw_graph(self, title="Chandigarh University Road Network (15 Locations, 25 Roads)"):
        self.ax.clear()
        self.ax.set_title(title, fontsize=11, fontweight="bold", pad=8, color="#1A237E")
        nx.draw_networkx_nodes(self.nx_g, COORDS, ax=self.ax, node_size=550, node_color="#1E88E5", edgecolors="#0D47A1")
        nx.draw_networkx_edges(self.nx_g, COORDS, ax=self.ax, edge_color="#B0BEC5", width=1.8, alpha=0.8)
        lbls = {i: f"{i}\n{LOCATIONS[i].split('(')[0].strip()}" for i in LOCATIONS}
        nx.draw_networkx_labels(self.nx_g, COORDS, labels=lbls, ax=self.ax, font_size=7, font_weight="bold")
        edge_lbls = {(u, v): f"{w}m" for u, v, w in EDGES}
        nx.draw_networkx_edge_labels(self.nx_g, COORDS, edge_labels=edge_lbls, ax=self.ax, font_size=6, font_color="#C62828")
        self.ax.axis("off")
        self.fig.tight_layout()
        self.canvas.draw()
        for k in self.labels:
            self.labels[k].config(text="--")
        self.log.delete("1.0", tk.END)
        self.log.insert(tk.END, "Ready. Select endpoints and click 'Run Algorithm'.\n")

    def run_algo(self):
        src, dest = self.get_nodes()
        choice = self.algo_cb.get()
        self.log.delete("1.0", tk.END)

        if "Dijkstra" in choice:
            res = self.engine.dijkstra(src, dest)
            self._render_path(res, src, dest, "#00C853")
        elif "BFS" in choice:
            res = self.engine.bfs(src, dest)
            self._render_path(res, src, dest, "#FF9800")
        elif "DFS" in choice:
            res = self.engine.dfs(src, dest)
            self._render_path(res, src, dest, "#9C27B0")
        elif "Kruskal" in choice:
            res = self.engine.kruskal()
            self._render_mst(res)
        elif "Prim" in choice:
            res = self.engine.prim(src)
            self._render_mst(res)
        else:
            self._compare_all(src, dest)

    def _render_path(self, res, src, dest, color):
        p, d = res["path"], res["dist"]
        self.labels["d"].config(text=f"{d:.1f} m" if d else "N/A")
        self.labels["h"].config(text=f"{res['hops']} hops")
        self.labels["t"].config(text=f"{res['time_us']} us")
        self.labels["o"].config(text=f"{res['ops']} ops")
        self.labels["tc"].config(text=res["tc"])
        self.labels["sc"].config(text=res["sc"])

        self.log.insert(tk.END, f"=== {res['algo'].upper()} ===\nRoute: {' -> '.join(map(str, p))}\n")
        self.log.insert(tk.END, f"Distance: {d}m | Hops: {res['hops']} | Time: {res['time_us']} us | Ops: {res['ops']}\n\nWaypoints:\n")
        for i, u in enumerate(p):
            self.log.insert(tk.END, f"  Step {i}: [{u}] {LOCATIONS[u]}\n")

        self.ax.clear()
        self.ax.set_title(f"{res['algo']}: Node {src} to {dest} | Dist: {d}m | Time: {res['time_us']} us",
                          fontsize=10, fontweight="bold", pad=8)
        nx.draw_networkx_nodes(self.nx_g, COORDS, ax=self.ax, node_size=500, node_color="#ECEFF1", edgecolors="#B0BEC5")
        nx.draw_networkx_edges(self.nx_g, COORDS, ax=self.ax, edge_color="#CFD8DC", width=1.5, style="dashed")

        if p and len(p) > 1:
            pe = list(zip(p[:-1], p[1:]))
            nx.draw_networkx_edges(self.nx_g, COORDS, edgelist=pe, ax=self.ax, edge_color=color, width=4)
            nx.draw_networkx_nodes(self.nx_g, COORDS, nodelist=p[1:-1], ax=self.ax, node_size=600, node_color=color)
            nx.draw_networkx_nodes(self.nx_g, COORDS, nodelist=[src], ax=self.ax, node_size=700, node_color="#2962FF")
            nx.draw_networkx_nodes(self.nx_g, COORDS, nodelist=[dest], ax=self.ax, node_size=700, node_color="#D50000")

        lbls = {i: f"{i}\n{LOCATIONS[i].split('(')[0].strip()}" for i in LOCATIONS}
        nx.draw_networkx_labels(self.nx_g, COORDS, labels=lbls, ax=self.ax, font_size=7, font_weight="bold")
        self.ax.axis("off")
        self.fig.tight_layout()
        self.canvas.draw()

    def _render_mst(self, res):
        mst, cost = res["mst"], res["cost"]
        self.labels["d"].config(text=f"{cost} m (MST)")
        self.labels["h"].config(text=f"{res['edges']} edges")
        self.labels["t"].config(text=f"{res['time_us']} us")
        self.labels["o"].config(text=f"{res['ops']} ops")
        self.labels["tc"].config(text=res["tc"])
        self.labels["sc"].config(text=res["sc"])

        self.log.insert(tk.END, f"=== {res['algo'].upper()} ===\nTotal Backbone Cost: {cost}m | Edges: {res['edges']}\n\nSelected Edges:\n")
        for u, v, w in mst:
            self.log.insert(tk.END, f"  ({u}) {LOCATIONS[u]:<20} <-> ({v}) {LOCATIONS[v]:<20} = {w}m\n")

        self.ax.clear()
        self.ax.set_title(f"{res['algo']} | Total Cost: {cost}m | Edges: {res['edges']} | Ops: {res['ops']}",
                          fontsize=10, fontweight="bold", pad=8)
        nx.draw_networkx_nodes(self.nx_g, COORDS, ax=self.ax, node_size=550, node_color="#FF6D00", edgecolors="#BF360C")
        nx.draw_networkx_edges(self.nx_g, COORDS, ax=self.ax, edge_color="#ECEFF1", width=1, style="dotted")
        pe = [(u, v) for u, v, _ in mst]
        nx.draw_networkx_edges(self.nx_g, COORDS, edgelist=pe, ax=self.ax, edge_color="#304FFE", width=3.5)
        lbls = {i: f"{i}\n{LOCATIONS[i].split('(')[0].strip()}" for i in LOCATIONS}
        nx.draw_networkx_labels(self.nx_g, COORDS, labels=lbls, ax=self.ax, font_size=7, font_weight="bold")
        mst_lbls = {(u, v): f"{w}m" for u, v, w in EDGES if (u, v) in pe or (v, u) in pe}
        nx.draw_networkx_edge_labels(self.nx_g, COORDS, edge_labels=mst_lbls, ax=self.ax, font_size=6.5, font_color="#D50000")
        self.ax.axis("off")
        self.fig.tight_layout()
        self.canvas.draw()

    def _compare_all(self, src, dest):
        d = self.engine.dijkstra(src, dest)
        b = self.engine.bfs(src, dest)
        df = self.engine.dfs(src, dest)
        k = self.engine.kruskal()
        p = self.engine.prim(src)

        data = [("Dijkstra", d["dist"], d["ops"], d["time_us"]),
                ("BFS", b["dist"], b["ops"], b["time_us"]),
                ("DFS", df["dist"], df["ops"], df["time_us"]),
                ("Kruskal", k["cost"], k["ops"], k["time_us"]),
                ("Prim", p["cost"], p["ops"], p["time_us"])]

        self.log.insert(tk.END, f"{'Algorithm':<10} | {'Distance/Cost':<14} | {'Operations':<10} | {'Time (us)':<10}\n" + "-"*50 + "\n")
        for name, dist, ops, tm in data:
            self.log.insert(tk.END, f"{name:<10} | {dist if dist else 'N/A':<14} | {ops:<10} | {tm:<10.2f}\n")

        self.ax.clear()
        x, width = range(len(data)), 0.35
        names, times, ops_list = [row[0] for row in data], [row[3] for row in data], [row[2] for row in data]
        self.ax.set_title(f"Algorithm Benchmark (Node {src} to {dest})", fontsize=10, fontweight="bold")
        self.ax.bar([i - width/2 for i in x], times, width, label="Time (us)", color="#1976D2")
        self.ax.set_ylabel("Execution Time (us)", color="#1976D2")
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(names, fontweight="bold")
        ax2 = self.ax.twinx()
        ax2.bar([i + width/2 for i in x], ops_list, width, label="Ops", color="#FF8F00")
        ax2.set_ylabel("Operations Count", color="#FF8F00")
        self.fig.tight_layout()
        self.canvas.draw()

# ==============================================================================
# 6. CLI HEADLESS BENCHMARK / TEST RUNNER
# ==============================================================================

def run_cli():
    """Headless CLI benchmark displaying tabular algorithm performance."""
    print("=" * 72)
    print("SMART ROUTE OPTIMIZATION - GRAPH ALGORITHMS BENCHMARK (CLI)")
    print("=" * 72)
    g = CampusGraph(LOCATIONS, EDGES)
    eng = RouteEngine(g)
    results = [eng.dijkstra(0, 4), eng.bfs(0, 4), eng.dfs(0, 4), eng.kruskal(), eng.prim(0)]

    print(f"{'Algorithm':<14} | {'Cost/Distance':<14} | {'Time (us)':<10} | {'Ops':<8} | {'Complexity':<16}")
    print("-" * 72)
    for res in results:
        val = res.get('dist', res.get('cost'))
        val_str = f"{val:.1f} m" if val is not None else "N/A"
        print(f"{res['algo']:<14} | {val_str:<14} | {res['time_us']:<10.2f} | {res['ops']:<8} | {res['tc']:<16}")
    print("=" * 72)
    print("Execution verified. Run `python app.py` without arguments for GUI.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli()
    else:
        root = tk.Tk()
        app = App(root)
        root.mainloop()
