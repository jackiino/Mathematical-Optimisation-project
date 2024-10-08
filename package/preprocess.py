def preprocess(V, E, T, l):
    def get_adjacent_edges(node):
        return [(min(u, v), max(u, v)) for (u, v) in E if u == node or v == node]

    def get_adjacent_nodes(node):
        return set([v if u == node else u for (u, v) in E])

    def is_terminal_connected(v, adj_edges):
        return any(u in T or v in T for u, v in adj_edges)

    changed = True
    while changed:
        changed = False
        V_new, E_new, T_new = V.copy(), E.copy(), T.copy()

        for v in V:
            adjacent_edges = get_adjacent_edges(v)
            if v not in T and len(adjacent_edges) == 1:
                if not is_terminal_connected(v, adjacent_edges):
                    E_new = [e for e in E_new if v not in e]
                    V_new.remove(v)
                    changed = True

        for v in V:
            if v not in T:
                adj_edges = get_adjacent_edges(v)
                edge_colors = {l.get((i, j), l.get((j, i))) for i, j in adj_edges}
                if len(adj_edges) > 1 and len(edge_colors) == 1:
                    if not is_terminal_connected(v, adj_edges):
                        E_new = [e for e in E_new if v not in e]
                        V_new.remove(v)
                        changed = True
        
        for t in T:
            adj_edges = get_adjacent_edges(t)
            colors = {l.get((i, j), l.get((j, i))) for i, j in adj_edges}
            if len(colors) == 1:
                color = colors.pop()
                edges_to_remove = [(i, j) for (i, j) in E_new 
                                   if (i != t and j != t) and l.get((i, j), l.get((j, i))) == color]
                E_new = [e for e in E_new if e not in edges_to_remove]
                changed = True        
        
        if not changed:
            break

        V, E, T = V_new, E_new, T_new

    return V, E, T