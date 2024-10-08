import time
import random as rn
import gurobipy as gb
from read_graph import *

class BestSolutionTracker:
    def __init__(self, model):
        self.start_time = time.time()  # Record the start time of optimization
        self.time_to_best = None  # To store the time when the best solution is found
        self.best_obj_val = float('inf')  # Initialize best objective value with infinity

    def callback(self, model, where):
        # Check for a new best solution
        if where == gb.GRB.Callback.MIPSOL:
            current_obj_val = model.cbGet(gb.GRB.Callback.MIPSOL_OBJ)

            # If the current solution is better than the previous best
            if current_obj_val < self.best_obj_val:
                self.best_obj_val = current_obj_val
                self.time_to_best = time.time() - self.start_time  # Record the time to best solution
                print(f"New best solution found with objective value: {self.best_obj_val}")
                print(f"Time to best solution: {self.time_to_best:.2f} seconds")


def solve_RSTP(V, E, c, l, T, s):
    # Set source as the first terminal
    s = rn.choice(T)

    # Exclude source node from terminal nodes
    T_ = [k for k in T if k != s]
    
    # Define both directions for edges
    A = E + [(j, i) for (i, j) in E]

    # Initialize model
    model = gb.Model("RSTP")
    
    # Decision variables
    x = model.addVars(E, vtype=gb.GRB.BINARY, name="x")
    f = model.addVars(A, T_, lb=0.0, name="f")
    
    # Objective function: Minimize total cost
    model.modelSense = gb.GRB.MINIMIZE
    model.setObjective(gb.quicksum(c[e] * x[e] for e in E))
    
    # Flow conservation constraints
    for i in V:
        for k in T_:
            model.addConstr(
                gb.quicksum(f[i, j, k] for j in V if (i, j) in A) - 
                gb.quicksum(f[j, i, k] for j in V if (j, i) in A) == 
                (1 if i == s else -1 if i == k else 0),
                name=f"flow_conservation_{i}_{k}"
            )
    
    # Flow-capacity linking constraints
    for (i, j) in E:
        for k in T_:
            model.addConstr(f[i, j, k] <= x[i, j], name=f"flow_capacity_{i}_{j}_{k}")
            model.addConstr(f[j, i, k] <= x[i, j], name=f"flow_capacity_{j}_{i}_{k}")
    
    # Rainbow condition constraints
    for p_value in set(l.values()):
        model.addConstr(
            gb.quicksum(x[e] for e in E if e in l and l[e] == p_value) <= 1,
            name=f"color_constraint_{p_value}"
        )
    
    # Set a longer time limit for optimization
    model.setParam('TimeLimit', 1800)  # Set the time limit to 600 seconds

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
        model.computeIIS()
        model.write("model.ilp")
    else:
        print(f"Optimization status: {model.status}")
        
        if model.SolCount > 0:  # Check if at least one solution has been found
            print(f"Best objective value found: {model.objVal if model.status == gb.GRB.OPTIMAL else tracker.best_obj_val}")
            print("Edges in the solution:")
            for e in E:
                if x[e].x > 0.5:
                    print(f"Edge {e} with cost {c[e]}")
            print("Flow values:")
            for (i, j) in A:
                for k in T_:
                    if f[i, j, k].x > 0:
                        print(f"Flow from {i} to {j} for commodity {k}: {f[i, j, k].x}")
        else:
            print("No feasible solution found within the time limit.")

        # Print the final time to the best solution found
        #print(f"Final time to best solution: {tracker.time_to_best:.2f} seconds")
        #print(f"Total time taken: {total_time_taken:.2f} seconds")

    # Return both the best objective value (final or best found within time limit)
    # and the time to the best solution
    best_obj_val = model.objVal if model.status == gb.GRB.OPTIMAL else tracker.best_obj_val
    return best_obj_val, tracker.time_to_best, total_time_taken

'''
# Function to generate input objects (assuming the file parser exists)
def generate_input_objects(file_path):
    num_nodes, edges, costs, colors, terminals = parse_stp_file(file_path)

    V = list(range(num_nodes))
    E = edges
    c = costs
    l = colors
    T = terminals

    return V, E, c, l, T
'''