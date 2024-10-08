import heapq

def dijkstra_bidirectional(source, V, A, k, modified_cost):
        dist = {v: float('inf') for v in V}
        dist[source] = 0
        prev = {v: None for v in V}
        pq = [(0, source)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for (u_, v) in A:
                if u_ == u:
                    # Use the modified cost with the Lagrangian multiplier for terminal k
                    alt = dist[u] + modified_cost(u, v, k)
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        heapq.heappush(pq, (alt, v))
        return dist, prev