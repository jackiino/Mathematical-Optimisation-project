import re

def parse_stp_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract number of nodes
    nodes_match = re.search(r'Nodes (\d+)', content)
    num_nodes = int(nodes_match.group(1)) if nodes_match else 0

    # Extract edges, costs, and colors
    edge_matches = re.findall(r'E (\d+) (\d+) (\d+) (\d+)', content)
    edges = [(int(m[0])-1, int(m[1])-1) for m in edge_matches]
    costs = {(int(m[0])-1, int(m[1])-1): int(m[2]) for m in edge_matches}
    colors = {(int(m[0])-1, int(m[1])-1): int(m[3]) for m in edge_matches}

    # Extract terminals
    terminal_matches = re.findall(r'T (\d+)', content)
    terminals = [int(t)-1 for t in terminal_matches]

    return num_nodes, edges, costs, colors, terminals

def generate_input_objects(file_path):
    num_nodes, edges, costs, colors, terminals = parse_stp_file(file_path)

    V = list(range(num_nodes))
    E = edges
    c = costs
    l = colors
    T = terminals

    return V, E, c, l, T