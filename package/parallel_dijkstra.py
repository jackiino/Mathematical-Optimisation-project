import concurrent.futures
from dijkstra_bidirectional import *


def parallel_dijkstra(source, V, A, T, mu, modified_cost, reconstruct_path_with_flow):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(dijkstra_bidirectional, source, V, A, k, modified_cost): k for k in T if k != source}
            results = {}
            for future in concurrent.futures.as_completed(futures):
                k = futures[future]
                distances, prev = future.result()
                path, flow = reconstruct_path_with_flow(prev, k, A)
                results[k] = {'distance': distances[k], 'path': path, 'flow': flow}
        return results