def construct_subgraph(A, x, c_bidirectional, p_bidirectional):
            N = set()
            p_bar = {}
            A_bar = set()
            c_bar = {}

            for (i, j) in A:
                # Ensure that we only consider one direction of an undirected edge
                if x.get((i, j), 0) == 1 or x.get((j, i), 0) == 1:
                    N.add(i)
                    N.add(j)

                    # Check if the edge (i, j) or (j, i) is already added to A_bar
                    if (i, j) not in A_bar and (j, i) not in A_bar:
                        A_bar.add((i, j))  # Add edge in only one direction
                        c_bar[(i, j)] = c_bidirectional[(i, j)]
                        p_bar[(i, j)] = p_bidirectional[(i, j)]

            for (i, j) in A:
                if i in N and j in N:
                    if (i, j) not in A_bar and (j, i) not in A_bar: 
                        A_bar.add((i, j))
                        c_bar[(i, j)] = c_bidirectional[(i, j)]
                        p_bar[(i, j)] = p_bidirectional[(i, j)]
                        
            if len(A_bar) == 0:
                print("Warning: Empty subgraph detected!")

            return list(N), list(A_bar), p_bar, c_bar