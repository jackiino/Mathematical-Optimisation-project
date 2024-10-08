from collections import namedtuple
import random


# Label structure
Label = namedtuple('Label', ['direction', 's', 'c', 'L', 'path'])

def dominates(y1, y2):
    """Check if label y1 dominates label y2."""
    return (y1.s == y2.s and 
            y1.direction == y2.direction and 
            y1.c <= y2.c and 
            set(y1.L).issubset(set(y2.L))) 

def can_be_feasibly_joined(y1, y2):
    """Check if two labels can be feasibly joined."""
    # Check if there is at least one node in common between the two paths
    common_nodes = set(y1.path).intersection(set(y2.path))
    
    # Ensure that the labels are in different directions, and there is no color overlap
    return (y1.direction != y2.direction and 
            common_nodes and  # Ensure there is at least one common node
            set(y1.L).isdisjoint(set(y2.L)))  # Ensure no color overlap

def get_components(S, e):
    """
    Get two components after removing edge e from the set S.
    
    Parameters:
    S (set of tuples): The current solution set of edges.
    e (tuple): The edge to be removed.

    Returns:
    C1 (set): The set of nodes in the first component.
    C2 (set): The set of nodes in the second component.
    """
    # Step 1: Remove edge e from the set of edges S
    S_prime = S.copy()
    S_prime.remove(e)

    # Step 2: Find the two connected components
    # We know e = (u, v), and removing it may break the graph into two components
    u, v = e

    # Start a DFS/BFS from u to find all nodes connected to u
    def dfs(node, edges, visited):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                # Add neighbors (nodes connected by edges) to the stack
                for edge in edges:
                    if current in edge:
                        neighbor = edge[0] if edge[1] == current else edge[1]
                        if neighbor not in visited:
                            stack.append(neighbor)

    # Component C1 (reachable from node u)
    C1 = set()
    dfs(u, S_prime, C1)

    # Component C2 (everything else not in C1)
    all_nodes = set([node for edge in S for node in edge])
    C2 = all_nodes - C1

    return C1, C2

def is_connected(S, V):
    if not S:
        return False
    
    # Start the connected set with one of the vertices from V
    first_vertex = next(iter(V))  
    connected = set([first_vertex])
    
    while True:
        size = len(connected)
        for e in S:
            if e[0] in connected and e[0] in V:
                connected.add(e[1])
            if e[1] in connected and e[1] in V:
                connected.add(e[0])
        if len(connected) == size:
            break

    # Return True only if all vertices in V are connected
    return connected.issuperset(V)


def join(C1, C2, G, size):
    V, E, c, l = G
    L = []
    D = {n: [] for n in V}
    
    
    # Initialize the forward labels for C1
    for n in C1:
        y = Label('forward', n, 0, frozenset(), (n,))
        L.append(y)
        D[n].append(y)


    # Initialize the backward labels for C2
    for n in C2:
        y = Label('backward', n, 0, frozenset(), (n,))
        L.append(y)
        D[n].append(y)
        
    
    feasibles = []
    
    while L and len(feasibles) < size:
        yi = L.pop(0)

        # If yi is a forward path, check for backward joins
        if yi.direction == 'forward':
            for y in L:
                if y == yi:  # Skip yi itself
                    continue
        
                if y.direction == 'backward' and can_be_feasibly_joined(yi, y):
                    feasibles.append((yi, y))
                    continue

        else:
            for y in L:
                if y == yi:  # Skip yi itself
                    continue
        
                if y.direction == 'forward' and can_be_feasibly_joined(yi, y):
                    feasibles.append((yi, y))
                    continue
                        
                # Expand neighbors in both directions
        last_node = yi.path[-1]

                
        for t in V:
            if (last_node, t) in E or (t, last_node) in E:
                edge = (last_node, t) if (last_node, t) in E else (t, last_node)


                if (last_node, t) in l or (t, last_node) in l:
                    color_i = l[(last_node, t)] if (last_node, t) in l else l[(t, last_node)]
               

                # Prevent loops by checking if t is already in the path
                if t in yi.path:
                    continue

                # Prevent reusing the same color by checking if color_i is in the path's color set
                if color_i in yi.L:
                    continue

                if (last_node, t) in l or (t, last_node) in l:
                    cost = c[(last_node, t)] if (last_node, t) in l else c[(t, last_node)]


                # Create a new label yt as a new independent object
                yt = Label(yi.direction, yi.s, yi.c + cost, 
                        yi.L | frozenset([color_i]), yi.path + (t,))


                # Ensure the new label is not dominated
                if not any(dominates(y, yt) for y in D[t]):
                    # Remove dominated labels
                    D[t] = [y for y in D[t] if not dominates(yt, y)]
                    L = [y for y in L if not dominates(yt, y)]
                    # Add yt to both L and D[t]
                    L.append(yt)
                    D[t].append(yt)
            
    return feasibles


def construct(G, T, size):
    V, E, c, l = G
    S = set()  # The solution set
    E_prime = E.copy()  # Create a copy of edges to modify

    # Start with a random terminal node
    start = random.choice(T)
    
    # Separate the terminals into two sets: C1 (connected terminals) and C2 (unconnected terminals)
    C1 = {start}
    C2 = set(T) - C1

    # Keep iterating until all terminals are connected (C2 is empty)
    while C2:
        # Call the join function to get feasible paths between C1 and C2
        F = join(C1, C2, (V, E_prime, c, l), size)

        # If join fails (no feasible paths found), return None
        if not F:
            return None
        
        # Strategy that selects the path with less colors
        #selected_path = min(F, key=lambda p: len(p[0].L | p[1].L))  # Minimize the union of colors in both directions

        # A pure greedy strategy selects the cheapest path in terms of cost
        #selected_path = min(F, key=lambda p: p[0].c + p[1].c)

        # A random strategy increases the diversity of the generated solutions
        selected_path = random.choice(F)

        # Extract the edges from the selected path (handling both directions)
        forward_path_edges = [(selected_path[0].path[i], selected_path[0].path[i + 1]) for i in range(len(selected_path[0].path) - 1)]
        backward_path_edges = [(selected_path[1].path[i], selected_path[1].path[i + 1]) for i in range(len(selected_path[1].path) - 1)]
        path_edges = forward_path_edges + backward_path_edges

        for edge in path_edges:
            S.add(edge)
            i, j = edge
            if (i,j) in E:
                edge_color = l[(i,j)]
            else:
                edge_color = l[(j,i)]

            E_prime = [(i, j) for (i, j) in E_prime if (l.get((i, j)) != edge_color and l.get((j, i)) != edge_color)]

            if edge[0] in T:
                C1.add(edge[0])
                C2.discard(edge[0])
            if edge[1] in T:
                C1.add(edge[1])
                C2.discard(edge[1])

    return S
        

def local_search(G, T, S):
    V, E, c, l = G
    E_prime = set(E.copy())  # Initialize E' as a set for set operations
    
    # Initialize E_prime by removing edges with the same color as those in S
    for edge in S:
        i, j = edge
        if (i, j) in E:
            edge_color = l[(i, j)]
        else:
            edge_color = l[(j, i)]

        E_prime = {e for e in E_prime if l.get(e) != edge_color and l.get((e[1], e[0])) != edge_color}
    
    updated = True

    while updated:
        updated = False
        for e in list(S):  # Iterate over a copy of S to modify S within the loop
            i, j = e
            if (i, j) in E:
                edge_color = l[(i, j)]
                edge_cost = c[(i, j)]
            else:
                edge_color = l[(j, i)]
                edge_cost = c[(j, i)]

            # Reinsert edges of the same color back into E_prime, except for edge e
            E_prime_with_color = {edge for edge in E if l.get(edge) == edge_color or l.get((edge[1], edge[0])) == edge_color}
            E_prime_with_color.discard(e)  # Remove the current edge from the set

            E_prime.update(E_prime_with_color)  # Union the sets to add back the color-related edges
            
            # Get the components created by removing edge e from S
            C1, C2 = get_components(S, e)
            
            # Attempt to find a feasible path to replace the removed edge
            feasibles = join(C1, C2, (V, E_prime, c, l), 1)
            
            if feasibles:
                # Select a random feasible path or the cheapest one
                selected_path = random.choice(feasibles)
                path_cost = selected_path[0].c + selected_path[1].c
            else:
                path_cost = float('inf')  # High cost if no feasible path is found
            
            # If the new path is cheaper than the current edge, update the solution
            if path_cost < edge_cost:
                # Remove the current edge from the solution
                S.remove(e)
                
                # Add the new path to the solution
                for i in range(len(selected_path[0].path) - 1):
                    S.add((selected_path[0].path[i], selected_path[0].path[i + 1]))
                for i in range(len(selected_path[1].path) - 1):
                    S.add((selected_path[1].path[i], selected_path[1].path[i + 1]))

                # Reinsert edges of the same color back into E_prime
                E_prime_with_color = {edge for edge in E if l.get(edge) == edge_color or l.get((edge[1], edge[0])) == edge_color}
                E_prime.update(E_prime_with_color)  # Update E_prime to reflect the changes
                
                updated = True  # Set flag to indicate the solution was updated
            else:
                # If no feasible path is found or path is not cheaper, restore E_prime
                E_prime = {edge for edge in E_prime if l.get(edge) != edge_color and l.get((edge[1], edge[0])) != edge_color}
    
    return S


def preprocess(V, E, T, l):
    def get_adjacent_edges(node):
        """Get all edges adjacent to a node."""
        return [(min(u, v), max(u, v)) for (u, v) in E if u == node or v == node]

    def get_adjacent_nodes(node):
        """Get all nodes adjacent to a node."""
        return set([v if u == node else u for (u, v) in E])

    def is_terminal_connected(v, adj_edges):
        """Check if the node is connected to a terminal."""
        return any(u in T or v in T for u, v in adj_edges)

    changed = True
    while changed:
        changed = False
        V_new, E_new, T_new = V.copy(), E.copy(), T.copy()


        # Test 1: Non-terminal with Degree 1 (NTD1)
        
        for v in V:
            adjacent_edges = get_adjacent_edges(v)
            if v not in T and len(adjacent_edges) == 1:
                # If this node is not a terminal and has only one edge, remove it only if it doesn't connect to a terminal
                if not is_terminal_connected(v, adjacent_edges):
                    E_new = [e for e in E_new if v not in e]
                    V_new.remove(v)
                    changed = True
        
        
        # Test 2: Non-terminal with 1 Color (NT1C)
        
        for v in V:
            if v not in T:
                adj_edges = get_adjacent_edges(v)
                edge_colors = set()
                for i, j in adj_edges:
                    if l.get((i, j)):
                        edge_colors.add(l.get((i, j)))
                    else:
                        edge_colors.add(l.get((j, i)))
                if len(adj_edges) > 1 and len(edge_colors) == 1:
                    # Only remove if the node doesn't connect to a terminal
                    if not is_terminal_connected(v, adj_edges):
                        E_new = [e for e in E_new if v not in e]
                        V_new.remove(v)
                        changed = True
        '''
        # Test 3: Terminal with 1 Degree (T1D)
        for t in T:
            adj_edges = get_adjacent_edges(t)
            edges_to_remove = []
            if len(adj_edges) == 1:
                i, j = adj_edges[0]  # Unpack the single adjacent edge correctly
                color_to_remove = l.get((i, j), l.get((j, i)))
                T_new.remove(t)
                if i == t:
                    T_new.append(j)
                else:
                    T_new.append(i)
                
                for e in E:
                    if l.get(e, l.get((min(e), max(e)))) == color_to_remove:
                        edges_to_remove.append(e)
                
            if edges_to_remove:
                # Update edge list by removing the identified edges
                E_new = [e for e in E_new if e not in edges_to_remove]
                changed = True  # A change occurred, so we continue
        '''
        
        
        # Test 4: Terminal with 1 Color (T1C)
        for t in T:
            adj_edges = get_adjacent_edges(t)
            colors = set()
            for i, j in adj_edges:
                if l.get((i, j)):
                    colors.add(l.get((i, j)))
                else:
                    colors.add(l.get((j, i)))
                                     
            if len(colors) == 1:  # If all adjacent edges have the same color
                color = colors.pop()
                edges_to_remove = []

                for (i, j) in E_new:
                    if (i != t and j != t) and l.get((i, j), l.get((j, i))) == color:
                        edges_to_remove.append((i, j))

                if edges_to_remove:
                    # Update edge list by removing the identified edges
                    E_new = [e for e in E_new if e not in edges_to_remove]
                    changed = True  # A change occurred, so we continue
            
        
        
        # If no changes occurred in this round, the loop will stop
        if not changed:
            break

        # Update the graph after changes
        V, E, T = V_new, E_new, T_new

    return V, E, T


def multi_start(G, T, max_iterations, size):
    V, E, c, l = G
    
    # Preprocess the graph to reduce unnecessary nodes and edges
    V, E, T = preprocess(V, E, T, l)

    G = (V, E, c, l)
    
    print(f"Number of nodes after preprocess is : {len(V)}. They are: {V}")
    print(f"Number of edges after preprocess is : {len(E)}. They are: {E}")
    print(f"Number of terminals after preprocess is : {len(T)}. They are: {T}")

    best = None
    cost_best = float('inf')  # Initialize to a large value
    
    for iteration in range(max_iterations):
        # Modify edge costs by multiplying with a random factor
        c_prime = {e: c[e] * random.uniform(1.00, 1.20) for e in E}
        G_prime = (V, E, c_prime, l)
        
        # Construct the solution using the modified graph
        S = construct(G_prime, T, size)
        
        # Skip the iteration if no solution is found
        if S is None:
            print(f"Iteration {iteration + 1}: No feasible solution found, skipping.")
            continue
        
        # Apply local search after construction
        S = local_search(G_prime, T, S)
        
        # Calculate the cost of the current solution
        cost_solution = 0
        if S is not None:
            for (i, j) in S:
                if (i, j) in c_prime:
                    cost_solution += c_prime[(i, j)]
                else:
                    cost_solution += c_prime[(j, i)]
        
        # Update the best solution if the current one is better
        if best is None or cost_solution < cost_best:
            best = S.copy()  # Store the best solution found
            cost_best = cost_solution  # Update cost_best with the current best solution's cost
        
        # Print the best cost so far at each iteration
        print(f"Iteration {iteration + 1}: Best cost so far = {cost_best}")

    cost_real_solution = 0
    if best is not None:
            for (i, j) in best:
                if (i, j) in c_prime:
                    cost_solution += c[(i, j)]
                else:
                    cost_solution += c[(j, i)]

    # Final output of the best solution found
    return cost_real_solution

