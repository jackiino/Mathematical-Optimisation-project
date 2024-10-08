def algorithm_1(E, c, mu, color_map, x, T, s):
        reduced_costs = {}
        for color in color_map:
            min_edge = None
            min_cost = float('inf')
            for e in color_map[color]:
                i, j = e
                reduced_cost = c[e] - sum(mu.get((i, j, k), 0) for k in T if k != s)
                reduced_costs[e] = reduced_cost
                if reduced_cost < min_cost:
                    min_cost = reduced_cost
                    min_edge = e
            if min_cost < 0:
                x[min_edge] = 1
        return x, reduced_costs
