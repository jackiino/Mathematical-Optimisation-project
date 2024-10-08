from algorithm1 import *

def LR2(V, E, l, c, T, s, mu):
    x = {e: 0 for e in E}
    color_map = {}
    for edge, color in l.items():
        if color not in color_map:
            color_map[color] = []
        color_map[color].append(edge)

    selected_edges, reduced_costs = algorithm_1(E, c, mu, color_map, x, T, s)
    return selected_edges, reduced_costs  # Return x