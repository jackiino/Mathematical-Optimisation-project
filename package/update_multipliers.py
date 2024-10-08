import random

def update_multipliers(mu, flow_results, x, E, T, s, c):
    # epsilon = 0.9  # Small positive number for adjustments
    for (i, j) in E:
        for k in T:
            if k != s:
                flow_value = flow_results.get(k, {}).get((i, j), 0)
                x_value = x.get((i, j), 0)

                if flow_value == 0 and x_value == 1:
                    delta = c[(i, j)] - mu.get((i, j, k), 0)
                    epsilon = random.uniform(0,delta)
                    mu[(i, j, k)] = max(0, mu.get((i, j, k), 0) + delta - epsilon)

                elif flow_value > 0 and x_value == 0:
                    delta = mu.get((i, j, k), 0) - c[(i, j)]
                    epsilon = random.uniform(0,delta)
                    mu[(i, j, k)] = max(0, mu.get((i, j, k), 0) - delta + epsilon)

    return mu