from collections import namedtuple
from collections import namedtuple
import heapq
import random

# Label structure
Label = namedtuple('Label', ['direction', 's', 'c', 'L', 'path'])

def dominates(y1, y2):
    """Check if label y1 dominates label y2 with early exit."""
    if y1.s != y2.s or y1.direction != y2.direction or y1.c > y2.c:
        return False
    return y1.L.issubset(y2.L)

def can_be_feasibly_joined(y1, y2):
    """Check if two labels can be feasibly joined."""
    common_nodes = set(y1.path).intersection(set(y2.path))
    return (y1.direction != y2.direction and 
            common_nodes and  
            y1.L.isdisjoint(y2.L))

def get_components(S, e):
    """Get two components after removing edge e from the set S."""
    S_prime = S.copy()
    S_prime.remove(e)
    u, v = e

    def dfs(node, edges, visited):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for edge in edges:
                    if current in edge:
                        neighbor = edge[0] if edge[1] == current else edge[1]
                        if neighbor not in visited:
                            stack.append(neighbor)

    C1 = set()
    dfs(u, S_prime, C1)
    all_nodes = set([node for edge in S for node in edge])
    C2 = all_nodes - C1

    return C1, C2
'''
# Label structure
Label = namedtuple('Label', ['direction', 's', 'c', 'L', 'path'])

def dominates(y1, y2):
    """Check if label y1 dominates label y2 with early exit."""
    if y1.s != y2.s or y1.direction != y2.direction:
        return False
    if y1.c > y2.c:
        return False
    return y1.L.issubset(y2.L)  # Use frozenset directly for faster comparison


def can_be_feasibly_joined(y1, y2):
    """Check if two labels can be feasibly joined."""
    common_nodes = set(y1.path).intersection(set(y2.path))
    return (y1.direction != y2.direction and 
            common_nodes and  
            set(y1.L).isdisjoint(set(y2.L))) 

def get_components(S, e):
    """Get two components after removing edge e from the set S."""
    S_prime = S.copy()
    S_prime.remove(e)
    u, v = e

    def dfs(node, edges, visited):
        stack = [node]
        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for edge in edges:
                    if current in edge:
                        neighbor = edge[0] if edge[1] == current else edge[1]
                        if neighbor not in visited:
                            stack.append(neighbor)

    C1 = set()
    dfs(u, S_prime, C1)
    all_nodes = set([node for edge in S for node in edge])
    C2 = all_nodes - C1

    return C1, C2
'''