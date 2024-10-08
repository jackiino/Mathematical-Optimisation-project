def reconstruct_path_with_flow(prev, target, A):
        path = []
        flow = {(i, j): 0 for (i, j) in A}
        while target is not None:
            path.insert(0, target)
            if prev[target] is not None:
                i, j = prev[target], target
                flow[(i, j)] = 1
            target = prev[target]
        return path, flow