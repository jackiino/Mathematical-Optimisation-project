from parallel_dijkstra import *
from reconstruct_path import *

def LR1(V, E, l, c, T, s, mu):
    A = E + [(j, i) for (i, j) in E]  # Bidirectional edges
    c_bidirectional = c.copy()

    # Include reverse direction costs for bidirectional edges
    for (i, j) in E:
        c_bidirectional[(j, i)] = c[(i, j)]

    # Modified cost that includes the Lagrangian multiplier mu_{(i,j,k)} for each terminal node k
    def modified_cost(i, j, k):
        return mu.get((i, j, k), 0)

    # Execute parallelized Dijkstra for all terminal nodes except source
    results = parallel_dijkstra(s, V, A, T, mu, modified_cost, reconstruct_path_with_flow)

    # Extract and return the flow results for each terminal node
    flow_results = {k: results[k]['flow'] for k in T if k != s}

    return flow_results
