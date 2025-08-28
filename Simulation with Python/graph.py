import heapq

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}
        self.graph[u][v] = weight
        self.graph[v][u] = weight  # Since the graph is undirected

    def dijkstra(self, start, end):
        queue = [(0, start)]
        distances = {node: float('infinity') for node in self.graph}
        distances[start] = 0
        shortest_path = {node: None for node in self.graph}

        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_node == end:
                break
            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    shortest_path[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        return distances, shortest_path
