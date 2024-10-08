import os
import csv
import sys
import datetime  # Import for getting the current time

package_path = os.path.join(os.path.dirname(__file__), 'package')
sys.path.append(package_path)

from solve_RSTP import *
from LR import Lagrangian_Relaxation
from MA_hyperparameters import *
from multistart1 import *

if __name__ == '__main__': 
    folder_path = "./Instances_scalability/Instances"
    result_folder = "./Results"  # Specify the folder to save CSV files

    # Create the result folder if it doesn't exist
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    # Define CSV file paths within the result folder
    csv_file_exact = os.path.join(result_folder, "scalability_exact.csv")
    csv_file_LR = os.path.join(result_folder, "scalability_LR.csv")
    csv_file_MA = os.path.join(result_folder, "scalability_MA.csv")

    # Open CSV files for writing results
    with open(csv_file_exact, mode='w', newline='') as exact_file, \
         open(csv_file_LR, mode='w', newline='') as lr_file, \
         open(csv_file_MA, mode='w', newline='') as ma_file:

        exact_writer = csv.writer(exact_file)
        lr_writer = csv.writer(lr_file)
        ma_writer = csv.writer(ma_file)

        # Write headers for CSV files, including 'Start Time'
        exact_writer.writerow(['Algorithm', 'File', 'Result', 'Time Taken (seconds)', 'TtB', 'Start Time'])
        lr_writer.writerow(['Algorithm', 'File', 'Result', 'Time Taken (seconds)', 'TtB', 'Start Time'])
        ma_writer.writerow(['Algorithm', 'File', 'Result', 'Time Taken (seconds)', 'TtB', 'Start Time'])

        # Iterate over files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.stp'):  # Only process '.stp' files
                file_path = os.path.join(folder_path, filename)
                V, E, c, l, T = generate_input_objects(file_path)
                print(f"Processing file: {filename}")
                
                # Run the exact algorithm
                start_time_exact = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"Running exact algorithm on {filename} at {start_time_exact}")
                best_obj_val, time_to_best, total_time_taken = solve_RSTP(V, E, c, l, T, None)
                exact_writer.writerow(['Gurobi', filename, best_obj_val, total_time_taken, time_to_best, start_time_exact])
                
                
                # Run the Multi-start algorithm
                start_time_MA = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"Running MA algorithm on {filename} at {start_time_MA}")
                results_iterations_folder = "./Results_iterations_MA"

                if not os.path.exists(results_iterations_folder):
                    os.makedirs(results_iterations_folder)

                best_cost, avg_time_to_best, avg_total_time = run_experiment_for_file(V, E, c, l, T, file_path, results_iterations_folder)
                ma_writer.writerow(['Multi-Start', filename, best_cost, avg_total_time, avg_time_to_best, start_time_MA])
                
                # Run the Lagrangian Relaxation algorithm
                start_time_LR = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"Running LR algorithm on {filename} at {start_time_LR}")
                results_iterations_folder = "./Results_iterations_LR"

                if not os.path.exists(results_iterations_folder):
                    os.makedirs(results_iterations_folder)

                avg_UB, avg_time_to_best, avg_total_time = Lagrangian_Relaxation(V, E, c, l, T, None, file_path, results_iterations_folder)
                lr_writer.writerow(['Lagrangian Relaxation', filename, avg_UB, avg_total_time, avg_time_to_best, start_time_LR])
                
    print(f"Processing complete. Results saved in {result_folder}.")
