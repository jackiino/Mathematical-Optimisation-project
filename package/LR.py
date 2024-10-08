import csv
import random
import time
from LR1 import *
from LR2 import *
from update_multipliers import *
from solve_LR import *
from LR_hyperparameters import max_iterations, convergence_threshold, max_time, threshold
from read_graph import *
import os
from update import *
from construct_subgraph import *

def Lagrangian_Relaxation(V, E, c, l, T, s, file_path, result_folder):
    s = random.choice(T)  # Random source selection

    best_time_to_solution = None  # Initialize the best time to solution variable
    mu = {}
    UB = float('inf')  # Initialize the upper bound with infinity
    T_ = [k for k in T if k != s]

    # Initialize dual variables (mu)
    for k in T_:
        for (i, j) in E:
            mu[i, j, k] = c[(i, j)]

    A = E + [(j, i) for (i, j) in E]  # Make bidirectional edges
    c_bidirectional = c.copy()
    p_bidirectional = l.copy()

    for (i, j) in E:
        c_bidirectional[(j, i)] = c[(i, j)]
        p_bidirectional[(j, i)] = l[(i, j)]

    # Accumulators for time to best, total time, and UB
    times_to_best = []
    total_times = []
    best_UBs = []

    # Store iteration results for CSV
    iteration_results = []

    iteration = 0
    start_time = time.time()  # Track time for time-based stopping

    previous_objVal = float('inf')
    count_threshold = 0

    while iteration <= max_iterations and time.time() - start_time < max_time:
        flow_results = LR1(V, E, c, l, T, s, mu)
        selected_edges, reduced_costs = LR2(V, E, c, l, T, s, mu)

        x = update_x_based_on_flow(flow_results, A, selected_edges)

        # Update multipliers based on the flow and edge selection
        mu = update_multipliers(mu, flow_results, x, E, T, s, c_bidirectional)
            
        N, A_bar, p_bar, c_bar = construct_subgraph(A, x, c_bidirectional, p_bidirectional)

        objVal, x, f, time_to_best, total_time_taken = solve_Lagrange_Relaxtion(N, A_bar, p_bar, c_bar, T, s)

        if objVal:
            if objVal < UB:
                UB = objVal
                if best_time_to_solution is None or time_to_best < best_time_to_solution:
                    best_time_to_solution = time_to_best
                    print(f"New global best solution found at iteration {iteration}: {UB} (Time: {best_time_to_solution:.2f}s)")

            # Store the time to best, total time, and best UB for averaging
            time_taken = time.time() - start_time
            times_to_best.append(time_to_best)
            total_times.append(time_taken)
            best_UBs.append(UB)

            # Store each iteration's result
            iteration_results.append({
                "iteration": iteration,
                "time_to_best": time_to_best,
                "total_time": total_time_taken,
                "best_UB": UB
            })

            # Check for convergence
            if abs(previous_objVal - objVal) < convergence_threshold:
                count_threshold += 1
                if count_threshold == threshold:
                    print("Convergence achieved.")
                    break
        else:
            return None, None, None

        previous_objVal = objVal
        iteration += 1

    # Write results to CSV
    csv_filename = os.path.basename(file_path).replace('.stp', '')  # Get the file name without the extension
    csv_file_name = f'experiment_results_LR_{csv_filename}.csv'

    csv_filepath = os.path.join(result_folder, csv_file_name)

    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["iteration", "time_to_best", "total_time", "best_UB"])
        writer.writeheader()
        writer.writerows(iteration_results)

    # Compute averages
    average_time_to_best = sum(times_to_best) / len(times_to_best) if times_to_best else None
    average_total_time = sum(total_times) / len(total_times) if total_times else None
    average_best_UB = sum(best_UBs) / len(best_UBs) if best_UBs else None

    print(f"Final average time to best solution: {average_time_to_best:.2f} seconds")
    print(f"Final average total time: {average_total_time:.2f} seconds")
    print(f"Final average best UB: {average_best_UB:.2f}")
        
    # Return the averages
    return average_best_UB, average_time_to_best, average_total_time
