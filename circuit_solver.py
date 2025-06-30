# circuit_solver.py

import numpy as np

def solve_nodal(G, I):
    """Solve the linear system G·V = I to find node voltages."""
    return np.linalg.solve(G, I)

def build_network(resistors, current_sources):
    """
    resistors: list of tuples (node_a, node_b, ohms)
    current_sources: list of (node, current_in_amps)
    Ground = node 0, other nodes numbered 1...N
    """
    N = max(max(a, b) for a, b, _ in resistors)
    G = np.zeros((N, N))
    I = np.zeros(N)
    for a, b, R in resistors:
        conductance = 1.0 / R
        if a > 0:
            G[a-1, a-1] += conductance
        if b > 0:
            G[b-1, b-1] += conductance
        if a > 0 and b > 0:
            G[a-1, b-1] -= conductance
            G[b-1, a-1] -= conductance

    for node, current in current_sources:
        I[node-1] += current

    return G, I

def main():
    # Hypothetical 8‑node industrial sensor network
    resistors = [
        (1, 0, 1000), (2, 0, 2000), (3, 0, 1500),
        (1,2,500), (2,3,750), (3,4,1000),
        (4,5,1200), (5,6,1800), (6,7,2200)
    ]
    current_sources = [
        (1, -0.005), (3, 0.002), (5, -0.003), (7, 0.001)
    ]

    G, I = build_network(resistors, current_sources)
    V = solve_nodal(G, I)

    print(" Node Voltages in Simulated Sensor Network:")
    for idx, volts in enumerate(V, start=1):
        print(f" Node{idx}: {volts:.3f} V")

if __name__ == "__main__":
    main()
