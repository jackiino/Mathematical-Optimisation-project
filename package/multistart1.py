import os
from label import *
from statistics import mean
import csv
import time
import random
from construct import *
from concurrent.futures import ProcessPoolExecutor
from read_graph import *
from local_search import *
from concurrent.futures import ProcessPoolExecutor, TimeoutError

def multi_start(G, T, iterations, size, max_no_improvement=8, start_time=None, time_limit=None):
    V, E, c, l = G
    best = None
    cost_best = float('inf')
    time_to_best = None
    total_start_time = start_time if start_time else time.time()

    no_improvement_count = 0

    for iteration in range(iterations):
        # Check if global timeout was exceeded at the beginning of each iteration
        elapsed_time = time.time() - total_start_time
        if time_limit and elapsed_time > time_limit:
            print(f"Time limit of {time_limit} seconds exceeded. Returning the best result so far.")
            return best, cost_best, time_to_best

        print("Iteration: ", iteration)
        # Apply some randomization to edge costs for variability
        c_prime = {e: c[e] * random.uniform(0.8, 1.2) for e in E}
        G_prime = (V, E, c_prime, l)

        # Construct a new solution using randomized costs
        S = construct(G_prime, T, size)
        if S is None:
            continue

        S = local_search(G_prime, T, S)

        # Calculate cost based on original costs 'c'
        cost_solution = sum(c.get(e, c.get((e[1], e[0]))) for e in S)

        # Check if the current solution is better than the best one
        if best is None or cost_solution < cost_best:
            best = S.copy()
            cost_best = cost_solution
            time_to_best = time.time() - total_start_time
            no_improvement_count = 0  # Reset the no-improvement counter
        else:
            no_improvement_count += 1

        # If no improvement has been made for 'max_no_improvement' iterations, return early
        if no_improvement_count >= max_no_improvement:
            print(f"Stopping early after {iteration + 1} iterations due to no improvement.")
            return best, cost_best, time_to_best

    return best, cost_best, time_to_best

def parallel_multi_start_search(G, T, max_iterations, size, num_workers, time_limit):
    # Determine the number of iterations per worker
    iterations_per_worker = max_iterations // num_workers

    # Run the search in parallel using ProcessPoolExecutor
    best_solution = None
    best_cost = float('inf')
    best_time = None

    start_time = time.time()  # Track the start time of the search
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(multi_start, G, T, iterations_per_worker, size, start_time=start_time, time_limit=time_limit) for _ in range(num_workers)]
        
        try:
            # Loop through all futures and process the results within the time limit
            for future in futures:
                # Calculate remaining time dynamically and stop if time limit is reached
                remaining_time = time_limit - (time.time() - start_time)
                if remaining_time <= 0:
                    print("Global time limit reached. Cancelling remaining tasks.")
                    break  # Break the loop and cancel remaining tasks

                # Set a timeout for future.result()
                result = future.result(timeout=remaining_time)
                
                if result is not None:
                    solution, cost, time_to_best = result
                    if cost < best_cost:
                        best_solution = solution
                        best_cost = cost
                        best_time = time_to_best

        except TimeoutError:
            print("Task exceeded the time limit and was terminated.")

        # Cancel remaining tasks if time has exceeded or future hasn't completed yet
        for future in futures:
            if not future.done():
                future.cancel()

    return best_solution, best_cost, best_time


def run_experiment_for_file(V, E, c, l, T, file_path, result_folder, global_time_limit=600):
    # Load the graph from the given file path
    num_runs = 2
    results = []

    for run in range(num_runs):
        print("Run: ", run)
        # Track the start time of the run
        run_start_time = time.time()

        # Enforce a time limit per run or globally
        remaining_time = global_time_limit - (time.time() - run_start_time)
        if remaining_time <= 0:
            print("Global time limit reached. Stopping experiment.")
            break

        # Run the parallel search algorithm with the remaining time
        best_solution, best_cost, best_time = parallel_multi_start_search(
            (V, E, c, l), T, max_iterations=30, size=3, num_workers=3, time_limit=remaining_time)

        # Track the total time taken for the run
        total_time = time.time() - run_start_time

        if best_cost is None or best_time is None:
            continue

        # Save the results for this run, including the total time
        results.append((best_cost, best_time, total_time))

    if not results:
        print("No solution found in this run.")
        return None, None, None

    avg_cost = mean([result[0] for result in results])
    avg_time_to_best = mean([result[1] for result in results])
    avg_total_time = mean([result[2] for result in results])

    # Save results and averages to a CSV file named after the instance
    base_filename = os.path.basename(file_path).replace('.stp', '')  # Get the file name without the extension
    csv_filename = f'experiment_results_MA_{base_filename}.csv'

    csv_filepath = os.path.join(result_folder, csv_filename)

    with open(csv_filepath, 'w', newline='') as csvfile:
        fieldnames = ['Run', 'Best Cost', 'Total Time', 'Time To Best (TtB)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, (cost, time_to_best, total_time) in enumerate(results, start=1):
            writer.writerow({'Run': i, 'Best Cost': cost, 'Total Time': total_time, 'Time To Best (TtB)': time_to_best})

        # Write the averages as a final row
        writer.writerow({'Run': 'Average', 'Best Cost': avg_cost, 'Total Time': avg_total_time, 'Time To Best (TtB)': avg_time_to_best})

    return avg_cost, avg_time_to_best, avg_total_time
