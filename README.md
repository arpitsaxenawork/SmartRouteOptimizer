# Smart Route Optimization Using Graph Algorithms

A graph-theoretic route optimization application developed for **Design and Analysis of Algorithms (DAA)** (MCA 1st Semester, Chandigarh University).

The application simulates a 15-node, 25-edge road network representing the **Chandigarh University (CU)** campus. It demonstrates foundational DAA concepts including greedy choice properties, cut property, disjoint sets, and queue/stack traversals.

---

## Features

- **15 Campus Locations & 25 Weighted Road Segments**: Realistic road distances (in meters) and 2D spatial layout.
- **Dual Graph Data Structures**: Full Adjacency List ($O(V + E)$) and Adjacency Matrix ($O(V^2)$) representations.
- **Custom Algorithm Implementations (No Library Solvers)**:
  1. **Dijkstra's Algorithm**: Single-source shortest path using a Binary Min-Heap (`heapq`).
  2. **Breadth-First Search (BFS)**: Unweighted shortest hop path using a FIFO Queue (`collections.deque`).
  3. **Depth-First Search (DFS)**: Exploratory pathfinding with backtracking.
  4. **Kruskal's Algorithm**: Minimum Spanning Tree using Disjoint Set Union (DSU) with Path Compression and Union by Rank.
  5. **Prim's Algorithm**: Minimum Spanning Tree using priority queue-driven greedy cut expansion.
- **Interactive Tkinter Desktop GUI**:
  - Dropdown selection of source and target locations.
  - Interactive embedded Matplotlib canvas with path and MST highlighting.
  - Real-time performance metrics: Distance (meters), Hops, Execution Time ($\mu\text{s}$), Operation Count, and Big-O Complexities.
- **CLI Mode**: Run headlessly for quick batch benchmarks and tests.
- **Strict Code Constraint**: Complete implementation in under 500 lines of clean Python code.

---

## Complexity Summary

| Algorithm | Paradigm | Time Complexity | Space Complexity | Optimality Guarantee |
| :--- | :--- | :---: | :---: | :---: |
| **Dijkstra's Algorithm** | Greedy (Min-Heap) | $O((V + E) \log V)$ | $O(V)$ | Optimal Weighted Distance |
| **Breadth-First Search (BFS)** | FIFO Queue | $O(V + E)$ | $O(V)$ | Minimum Hops / Turns |
| **Depth-First Search (DFS)** | Stack / Recursion | $O(V + E)$ | $O(V)$ | Exploratory Traversal |
| **Kruskal's Algorithm** | Greedy (Edge-centric DSU) | $O(E \log E)$ | $O(V + E)$ | Optimal Minimum Spanning Tree |
| **Prim's Algorithm** | Greedy (Vertex cut-heap) | $O((V + E) \log V)$ | $O(V + E)$ | Optimal Minimum Spanning Tree |

---

## Installation & Usage

### 1. Prerequisites
Ensure Python 3.8+ is installed with `tkinter` support.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Interactive GUI
```bash
python app.py
```

### 4. Run Headless CLI Benchmark
```bash
python app.py --cli
```

---

## Project Structure

```
SmartRouteOptimizer/
├── app.py              # Complete application (Graph, Engine, GUI, CLI in < 500 lines)
├── requirements.txt    # Python dependencies (networkx, matplotlib)
├── .gitignore          # Git ignore file
└── README.md           # Project documentation
```

---

## Author
- **Arpit Saxena** (MCA Data Science, Chandigarh University)
- GitHub: [@arpitsaxenawork](https://github.com/arpitsaxenawork)
