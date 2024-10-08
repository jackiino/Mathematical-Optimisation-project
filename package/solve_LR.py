import gurobipy as gb
import time
import random as rn
from read_graph import *


def get_bidirectional_edges(E):
    return list(set(E + [(j, i) for (i, j) in E]))

class BestSolutionTracker:
    def __init__(self, model):
        self.start_time = time.time()  # Start time of optimization
        self.time_to_best = None  # Time to best solution
        self.best_obj_val = float('inf')  # Initialize with infinity
        self.global_best_obj_val = float('inf')  # Track global best

    def callback(self, model, where):
        if where == gb.GRB.Callback.MIPSOL:
            current_obj_val = model.cbGet(gb.GRB.Callback.MIPSOL_OBJ)
            if current_obj_val < self.best_obj_val:
                self.best_obj_val = current_obj_val
                self.time_to_best = time.time() - self.start_time
                print(f"New best solution found with objective value: {self.best_obj_val}")
                print(f"Time to best solution: {self.time_to_best:.2f} seconds")

            # Track global best solution across iterations
            if current_obj_val < self.global_best_obj_val:
                self.global_best_obj_val = current_obj_val
                print(f"New global best solution: {self.global_best_obj_val}")


def solve_Lagrange_Relaxtion(N_bar, A_bar, p_bar, c_bar, T, s):
    T_ = [k for k in T if k != s]
    A = get_bidirectional_edges(A_bar)

    model = gb.Model("Lagrangian Relaxation")
    model.setParam('OutputFlag', 0)  # Disable Gurobi output, set to 1 for debugging

    # Decision variables for edges
    x = model.addVars(A_bar, vtype=gb.GRB.BINARY, name="x")
    f = model.addVars(A, T_, lb=0.0, name="f")

    # Objective function: Minimize total cost
    model.modelSense = gb.GRB.MINIMIZE
    model.setObjective(gb.quicksum(c_bar[e] * x[e] for e in A_bar))

    # Flow conservation constraints
    for i in N_bar:
        for k in T_:
            model.addConstr(
                gb.quicksum(f[i, j, k] for j in N_bar if (i, j) in A) - 
                gb.quicksum(f[j, i, k] for j in N_bar if (j, i) in A) == 
                (1 if i == s else -1 if i == k else 0),
                name=f"flow_conservation_{i}_{k}"
            )

    # Flow-capacity linking constraints
    for (i, j) in A_bar:
        for k in T_:
            model.addConstr(f[i, j, k] <= x[i, j], name=f"flow_capacity_{i}_{j}_{k}")
            model.addConstr(f[j, i, k] <= x[i, j], name=f"flow_capacity_{j}_{i}_{k}")

    # Rainbow condition constraints (color constraints)
    for p_value in set(p_bar.values()):
        model.addConstr(
            gb.quicksum(x[e] for e in A_bar if e in p_bar and p_bar.get(e) == p_value) <= 1,
            name=f"color_constraint_{p_value}"
        )

    # Set a longer time limit for optimization
    model.setParam('TimeLimit', 600)  # Set the time limit to 10 minutes

    # Set up the best solution tracker with callback
    tracker = BestSolutionTracker(model)

    # Track the total time for the optimization process
    total_start_time = time.time()

    # Optimize the model with the callback function
    model.optimize(tracker.callback)

    # Calculate total time taken
    total_time_taken = time.time() - total_start_time

    # Print solution and status
    if model.status == gb.GRB.INFEASIBLE:
        print("Model is infeasible. Diagnosing...")
        #model.computeIIS()
        #model.write("model.ilp")
        return None, None, None, None, None
    else:
        print(f"Optimization status: {model.status}")
        
        if model.SolCount == 0:  # Check if at least one solution has been found
            print("No feasible solution found within the time limit.")

        # Print the final time to the best solution found

    best_obj_val = model.objVal if model.status == gb.GRB.OPTIMAL else tracker.best_obj_val
    time_to_best = tracker.time_to_best if tracker.time_to_best is not None else None
    print("Time to best: ", time_to_best)

    return best_obj_val, x, f, time_to_best, total_time_taken