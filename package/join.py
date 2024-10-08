import heapq
import time
from label import *


import random


def join(C1, C2, G, size, timeout=100):
    """Optimized join using heaps and early exit strategies."""
    V, E, c, l = G
    D = {n: [] for n in V}
    forward_heap = []  # Separate heap for forward labels
    backward_heap = []  # Separate heap for backward labels
    feasibles = []

    # Record the start time
    start_time = time.time()

    # Initialize forward heap with labels from C1
    for n in C1:
        y = Label('forward', n, 0, frozenset(), (n,))
        heapq.heappush(forward_heap, (y.c, y))
        D[n].append(y)

    # Initialize backward heap with labels from C2
    for n in C2:
        y = Label('backward', n, 0, frozenset(), (n,))
        heapq.heappush(backward_heap, (y.c, y))
        D[n].append(y)

    while (forward_heap or backward_heap) and len(feasibles) < size:
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            return feasibles if feasibles else None

        # Choose the smaller heap to pop from
        if not forward_heap:  # If the forward heap is empty, pop from the backward heap
            break
            #_, yi = heapq.heappop(backward_heap)
        elif not backward_heap:  # If the backward heap is empty, pop from the forward heap
            break
            #_, yi = heapq.heappop(forward_heap)
        else:  # Otherwise, pop from the heap with fewer elements
            if len(forward_heap) <= len(backward_heap):
                _, yi = heapq.heappop(forward_heap)
            else:
                _, yi = heapq.heappop(backward_heap)

        # Check for feasibles by comparing elements from the other heap
        other_heap = backward_heap if yi.direction == 'forward' else forward_heap
        for _, y in other_heap:
            if can_be_feasibly_joined(yi, y):
                feasibles.append((yi, y))

        last_node = yi.path[-1]
        path_set = set(yi.path)

        # Expand the current label to new nodes in the graph
        for t in V:
            if (last_node, t) in E or (t, last_node) in E:
                color_i = l.get((last_node, t), l.get((t, last_node)))
                if t in path_set or color_i in yi.L:
                    continue

                cost = c.get((last_node, t), c.get((t, last_node)))
                yt = Label(yi.direction, yi.s, yi.c + cost, yi.L | frozenset([color_i]), yi.path + (t,))

                # Ensure the new label is not dominated
                if not any(dominates(y, yt) for y in D[t]):
                    D[t] = [y for y in D[t] if not dominates(yt, y)]
                    if yt.direction == 'forward':
                        heapq.heappush(forward_heap, (yt.c, yt))
                    else:
                        heapq.heappush(backward_heap, (yt.c, yt))
                    D[t].append(yt)

    return feasibles if feasibles else None


'''
def join(C1, C2, G, size):
    V, E, c, l = G
    L = []
    D = {n: [] for n in V}    
    
    # Initialize the forward labels for C1
    for n in C1:
        y = Label('forward', n, 0, frozenset(), (n,))
        L.append(y)
        D[n].append(y)

    # Initialize the backward labels for C2
    for n in C2:
        y = Label('backward', n, 0, frozenset(), (n,))
        L.append(y)
        D[n].append(y)

    feasibles = []
    
    while L and len(feasibles) < size:
        #print("L: ", L)
        #yi = L.pop(0)

        #random_index = random.randint(0, len(L) - 1)
        #yi = L.pop(random_index)

        # Dynamically choose the direction based on label count
        forward_labels = [y for y in L if y.direction == 'forward']
        backward_labels = [y for y in L if y.direction == 'backward']

        # If both forward and backward labels are empty, break the loop
        if not forward_labels and not backward_labels:
            break  # No more labels to process

        # If one direction is empty, choose the other direction
        if not forward_labels:
            break
            #yi = min(backward_labels, key=lambda y: y.c)  # Expand backward label with least cost
        elif not backward_labels:
            break
            #yi = min(forward_labels, key=lambda y: y.c)  # Expand forward label with least cost
        else:
            # Choose the direction with fewer unprocessed labels
            if len(forward_labels) < len(backward_labels):
                yi = min(forward_labels, key=lambda y: y.c)  # Expand forward label with least cost
                #yi = min(forward_labels, key=lambda y: y.L)  # Expand forward label with less colours
                #random_index = random.randint(0, len(forward_labels) - 1)
                #yi = forward_labels.pop(random_index)
                #print("Selecting forward yi: ", yi)
            else:
                yi = min(backward_labels, key=lambda y: y.c)  # Expand backward label with least cost
                #yi = min(forward_labels, key=lambda y: y.L)  # Expand forward label with less colours
                #random_index = random.randint(0, len(backward_labels) - 1)
                #yi = backward_labels.pop(random_index)
                #print("Selecting backward yi: ", yi)

        L.remove(yi)  # Remove selected label from the list

        # If yi is a forward path, check for backward joins
        if yi.direction == 'forward':
            for y in L:
                if y == yi:  # Skip yi itself
                    continue
        
                if y.direction == 'backward' and can_be_feasibly_joined(yi, y):
                    feasibles.append((yi, y))
                    continue

        else:
            for y in L:
                if y == yi:  # Skip yi itself
                    continue
        
                if y.direction == 'forward' and can_be_feasibly_joined(yi, y):
                    feasibles.append((yi, y))
                    continue
        
        # Expand neighbors in both directions
        last_node = yi.path[-1]

        #expanded = False 
        
        for t in V:
            if (last_node, t) in E or (t, last_node) in E:
                if (last_node, t) in l or (t, last_node) in l:
                    color_i = l[(last_node, t)] if (last_node, t) in l else l[(t, last_node)]
               
                # Prevent loops by checking if t is already in the path
                if t in yi.path:
                    continue

                # Prevent reusing the same color by checking if color_i is in the path's color set
                if color_i in yi.L:
                    continue

                if (last_node, t) in l or (t, last_node) in l:
                    cost = c[(last_node, t)] if (last_node, t) in l else c[(t, last_node)]

                # Create a new label yt as a new independent object
                yt = Label(yi.direction, yi.s, yi.c + cost, 
                        yi.L | frozenset([color_i]), yi.path + (t,))

                # Ensure the new label is not dominated
                if not any(dominates(y, yt) for y in D[t]):
                    # Remove dominated labels
                    D[t] = [y for y in D[t] if not dominates(yt, y)]
                    L = [y for y in L if not dominates(yt, y)]
                    # Add yt to both L and D[t]
                    L.append(yt)
                    D[t].append(yt)
                    #expanded = True

        #if not expanded:
        #    no_progress_counter += 1
        #else:
        #    no_progress_counter = 0  # Reset counter if progress is made

        # Break if we've made no progress for several iterations
        #if no_progress_counter > 0:
        #    print("No progress in label expansion. Terminating join process.")
        #    break

            
    return feasibles if feasibles else None
'''

'''
def join(C1, C2, G, size, timeout=100):
    V, E, c, l = G
    D = {n: [] for n in V}
    forward_heap = []  # Separate heap for forward labels
    backward_heap = []  # Separate heap for backward labels
    feasibles = []

    # Record the start time
    start_time = time.time()

    # Initialize forward heap with labels from C1
    for n in C1:
        y = Label('forward', n, 0, frozenset(), (n,))
        heapq.heappush(forward_heap, (y.c, y))
        D[n].append(y)

    # Initialize backward heap with labels from C2
    for n in C2:
        y = Label('backward', n, 0, frozenset(), (n,))
        heapq.heappush(backward_heap, (y.c, y))
        D[n].append(y)

    while (forward_heap or backward_heap) and len(feasibles) < size:
        # Check if the timeout has been reached
        if time.time() - start_time > timeout:
            return feasibles if feasibles else None

        # Choose the smaller heap to pop from
        if not forward_heap:  # If the forward heap is empty, pop from the backward heap
            break
            #_, yi = heapq.heappop(backward_heap)
        elif not backward_heap:  # If the backward heap is empty, pop from the forward heap
            break
            #_, yi = heapq.heappop(forward_heap)
        else:  # Otherwise, pop from the heap with fewer elements
            if len(forward_heap) <= len(backward_heap):
                _, yi = heapq.heappop(forward_heap)
            else:
                _, yi = heapq.heappop(backward_heap)

        # Check for feasibles by comparing elements from the other heap
        other_heap = backward_heap if yi.direction == 'forward' else forward_heap
        for y in other_heap:
            if y[1].direction != yi.direction and can_be_feasibly_joined(yi, y[1]):
                feasibles.append((yi, y[1]))

        last_node = yi.path[-1]

        #expanded = False 

        # Expand the current label to new nodes in the graph
        for t in V:
            if (last_node, t) in E or (t, last_node) in E:
                if (last_node, t) in l or (t, last_node) in l:
                    color_i = l[(last_node, t)] if (last_node, t) in l else l[(t, last_node)]
                if t in yi.path or color_i in yi.L:
                    continue

                if (last_node, t) in l or (t, last_node) in l:
                    cost = c[(last_node, t)] if (last_node, t) in l else c[(t, last_node)]

                yt = Label(yi.direction, yi.s, yi.c + cost, 
                           yi.L | frozenset([color_i]), yi.path + (t,))
                if not any(dominates(y, yt) for y in D[t]):
                    D[t] = [y for y in D[t] if not dominates(yt, y)]
                    # Add the new label to the corresponding heap (forward or backward)
                    if yt.direction == 'forward':
                        heapq.heappush(forward_heap, (yt.c, yt))
                        expanded = True
                    else:
                        heapq.heappush(backward_heap, (yt.c, yt))
                        expanded = True
                    D[t].append(yt)


        #if not expanded:
        #    no_progress_counter += 1
        #else:
        #    no_progress_counter = 0  # Reset counter if progress is made

        # Break if we've made no progress for several iterations
        #if no_progress_counter > 10:
        #    print("No progress in label expansion. Terminating join process.")
        #    break

    return feasibles if feasibles else None
'''