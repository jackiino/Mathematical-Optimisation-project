from label import *
from join import *

def local_search(G, T, S):
    V, E, c, l = G
    E_prime = set(E.copy()) 

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
        
        # Step 1: Prioritize edges with the highest cost in the current solution
        edge_costs = []
        for e in S:
            i, j = e
            if (i, j) in E:
                edge_costs.append((e, c[(i, j)]))
            else:
                edge_costs.append((e, c[(j, i)]))
        
        # Sort edges by cost in descending order (to prioritize removing expensive edges)
        edge_costs.sort(key=lambda x: x[1], reverse=True)

        # Step 2: Try replacing edges starting from the most expensive one
        for e, edge_cost in edge_costs:
            i, j = e
            if (i, j) in E:
                edge_color = l[(i, j)]
            else:
                edge_color = l[(j, i)]

            # Reinsert edges of the same color back into E_prime, except for edge e
            E_prime_with_color = {edge for edge in E if l.get(edge) == edge_color or l.get((edge[1], edge[0])) == edge_color}
            
            if (i,j) in E:
                E_prime_with_color.discard((i,j))  # Remove the current edge from the set
            else:
                E_prime_with_color.discard((j,i))

            E_prime.update(E_prime_with_color)  # Union the sets to add back the color-related edges

            
            # Get the components created by removing edge e from S
            C1, C2 = get_components(S, e)
            
            # Attempt to find feasible paths to replace the removed edge
            feasibles = join(C1, C2, (V, E_prime, c, l), size=2)
            
            if feasibles:

                # Greedily select the path with the lowest total cost
                selected_path = min(feasibles, key=lambda p: p[0].c + p[1].c)
                path_cost = selected_path[0].c + selected_path[1].c
            else:
                path_cost = float('inf')  # High cost if no feasible path is found
            
            # If the new path is cheaper than the current edge, update the solution
            if path_cost < edge_cost:
                for (i,j) in S:
                    if (i,j) not in E_prime and (j,i) not in E_prime:
                        E_prime.add((i,j))

                S.remove(e)

                # Add the new path to the solution
                for i in range(len(selected_path[0].path) - 1):
                    S.add((selected_path[0].path[i], selected_path[0].path[i + 1]))
                for i in range(len(selected_path[1].path) - 1):
                    S.add((selected_path[1].path[i], selected_path[1].path[i + 1]))


                for (i,j) in S:
                    if (i,j) in E:
                        colour = l[(i,j)]
                    else:
                         colour = l[(j,i)]

                #E_prime_with_color = {edge for edge in S if l.get(edge) == edge_color or l.get((edge[1], edge[0])) == edge_color}
                
                to_remove = set()

                for (k, z) in E_prime:
                    if (k, z) in E:
                        if l[(k, z)] == colour:
                            to_remove.add((k, z))  # Mark for removal
                    else:
                        if l[(z, k)] == colour:
                            to_remove.add((z, k))  # Mark for removal

                # Now remove all the marked items after the iteration
                E_prime.difference_update(to_remove)

                #print()
                
                updated = True  # Set flag to indicate the solution was updated
                break  # Break out of the loop to start again with updated solution
            else:
                # If no feasible path is found or path is not cheaper, restore E_prime
                E_prime = {edge for edge in E_prime if l.get(edge) != edge_color and l.get((edge[1], edge[0])) != edge_color}
                #print("Togliamo da E_primo gli archi di colore uguale agli archi che non portano benefici")
    
    return S
