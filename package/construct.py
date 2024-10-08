import random
from join import *

def construct(G, T, size):
    """Construct solution by finding feasible joins between C1 and C2."""
    V, E, c, l = G
    S = set()
    E_prime = E.copy()
    start = random.choice(T)
    C1 = {start}
    C2 = set(T) - C1

    while C2:
        #print("C1: ", C1)
        #print("C2: ", C2)

        F = join(C1, C2, (V, E_prime, c, l), size)

        if not F:
            return None
        
        selected_path = random.choice(F)
        forward_path_edges = [(selected_path[0].path[i], selected_path[0].path[i + 1]) 
                              for i in range(len(selected_path[0].path) - 1)]
        backward_path_edges = [(selected_path[1].path[i], selected_path[1].path[i + 1]) 
                               for i in range(len(selected_path[1].path) - 1)]
        path_edges = forward_path_edges + backward_path_edges

        for edge in path_edges:
            i, j = edge
            if (i, j) not in S and (j, i) not in S:
                S.add(edge)
            edge_color = l.get((i, j), l.get((j, i)))
            E_prime = [(s, t) for (s, t) in E_prime 
                       if l.get((s, t), l.get((t, s))) != edge_color]

            if (i, j) not in E_prime and (j, i) not in E_prime:
                E_prime.append(edge)

            if edge[0] in T:
                C1.add(edge[0])
                C2.discard(edge[0])
            if edge[1] in T:
                C1.add(edge[1])
                C2.discard(edge[1])
                
    return S
'''
def construct(G, T, size):
    V, E, c, l = G
    S = set()
    E_prime = E.copy()
    start = random.choice(T)
    C1 = {start}
    C2 = set(T) - C1

    while C2:
        print("C1: ", C1)
        print("C2: ", C2)

        F = join(C1, C2, (V, E_prime, c, l), size)
        print("F: ", F)

        if not F:
            print("Not joinable")
            return None
        
        # A pure greedy strategy selects the cheapest path in terms of cost
        #selected_path = min(F, key=lambda p: p[0].c + p[1].c)

        selected_path = random.choice(F)

        forward_path_edges = [(selected_path[0].path[i], selected_path[0].path[i + 1]) 
                              for i in range(len(selected_path[0].path) - 1)]
        backward_path_edges = [(selected_path[1].path[i], selected_path[1].path[i + 1]) 
                               for i in range(len(selected_path[1].path) - 1)]
        path_edges = forward_path_edges + backward_path_edges

        for edge in path_edges:
            i, j = edge
            if (i, j) not in S and (j, i) not in S:
                S.add(edge)
            edge_color = l.get((i, j), l.get((j, i)))
            E_prime = [(s, t) for (s, t) in E_prime 
                       if l.get((s, t), l.get((t, s))) != edge_color]

            if (i, j) not in E_prime and (j, i) not in E_prime:
                E_prime.append(edge)

            if edge[0] in T:
                C1.add(edge[0])
                C2.discard(edge[0])
            if edge[1] in T:
                C1.add(edge[1])
                C2.discard(edge[1])
                
    return S
    '''