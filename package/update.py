def update_x_based_on_flow(flow_results, A, x):
            for k, flow in flow_results.items():
                for (i, j), f_value in flow.items():
                    if f_value > 0:
                        x[(i, j)] = 1  # Only update forward direction
            return x