import os
import csv
import sys

package_path = os.path.join(os.path.dirname(__file__), 'package')
sys.path.append(package_path)

from solve_RSTP import solve_RSTP
from multistart1 import *
from LR import Lagrangian_Relaxation
from MA_hyperparameters import *
from instance_test import *

if __name__ == '__main__':
    result_folder = "./Results_test"  # Specify the folder to save CSV files
    file_path = "./instance_test"

    # Create the result folder if it doesn't exist
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # Define CSV file paths within the result folder
    csv_file_exact = os.path.join(result_folder, "test_exact.csv")
    csv_file_LR = os.path.join(result_folder, "test_LR.csv")
    csv_file_MA = os.path.join(result_folder, "test_MA.csv")

    try:
        # Open CSV files for writing results
        with open(csv_file_exact, mode='w', newline='') as exact_file, \
                open(csv_file_LR, mode='w', newline='') as lr_file, \
                open(csv_file_MA, mode='w', newline='') as ma_file:

            exact_writer = csv.writer(exact_file)
            lr_writer = csv.writer(lr_file)
            ma_writer = csv.writer(ma_file)

            # Write headers for CSV files
            exact_writer.writerow(['Algorithm', 'File', 'Result', 'Time Taken (seconds)', 'TtB'])
            lr_writer.writerow(['Algorithm', 'File', 'Result', 'Time Taken (seconds)', 'TtB'])
            ma_writer.writerow(['Algorithm', 'File', 'Result', 'Time Taken (seconds)', 'TtB'])

            print(f"Processing test")

            # Run the exact algorithm
            print(f"Running exact algorithm on test")
            best_obj_val, time_to_best, total_time_taken = solve_RSTP(V, E, c, l, T, None)
            exact_writer.writerow(['Gurobi', "test", best_obj_val, total_time_taken, time_to_best])

            # Run the Multi-start algorithm
            print(f"Running MA algorithm on test")
            results_iterations_folder = "./Results_iterations_test/MA"

            if not os.path.exists(results_iterations_folder):
                os.makedirs(results_iterations_folder)

            best_cost, avg_time_to_best, avg_total_time = run_experiment_for_file(V, E, c, l, T, file_path, results_iterations_folder)
            ma_writer.writerow(['Multi-Start', "test", best_cost, avg_total_time, avg_time_to_best])

            # Run the Lagrangian Relaxation algorithm
            print(f"Running LR algorithm on test")
            results_iterations_folder = "./Results_iterations_test/LR"

            if not os.path.exists(results_iterations_folder):
                os.makedirs(results_iterations_folder)

            avg_UB, avg_time_to_best, avg_total_time = Lagrangian_Relaxation(V, E, c, l, T, None, file_path, results_iterations_folder)
            lr_writer.writerow(['Lagrangian Relaxation', "test", avg_UB, avg_total_time, avg_time_to_best])

        print(f"Processing complete. Results saved in {result_folder}.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
