def reconstruct_path(shortest_path, start, end):
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = shortest_path[current_node]
    path.reverse()  # Reverse to get the correct order
    return path

def remove_random_edges(graph, num_edges_to_remove):
    import random
    removed_edges = []
    edges = [(u, v) for u in graph.graph for v in graph.graph[u]]
    random.shuffle(edges)
    for i in range(num_edges_to_remove):
        u, v = edges[i]
        if v in graph.graph[u]:
            del graph.graph[u][v]
            del graph.graph[v][u]
            removed_edges.append((u, v))
    return removed_edges
