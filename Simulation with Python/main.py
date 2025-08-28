import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import Graph
from utils import reconstruct_path, remove_random_edges


class RescueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Landslide Rescue System")

        self.graph = Graph()
        self.nx_graph = nx.Graph()  # For visualization
        self.initialize_graph()

        # User Inputs
        self.start_label = tk.Label(root, text="Start Location:")
        self.start_label.grid(row=0, column=0, padx=10, pady=10)
        self.start_entry = tk.Entry(root)
        self.start_entry.grid(row=0, column=1, padx=10, pady=10)

        self.end_label = tk.Label(root, text="Safe Zone Location:")
        self.end_label.grid(row=1, column=0, padx=10, pady=10)
        self.end_entry = tk.Entry(root)
        self.end_entry.grid(row=1, column=1, padx=10, pady=10)

        # Shortest Path Button
        self.shortest_button = tk.Button(root, text="Find Shortest Path", command=self.find_shortest_path)
        self.shortest_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Simulate Landslide Button
        self.landslide_button = tk.Button(root, text="Simulate Landslide", command=self.simulate_landslide)
        self.landslide_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Graph Display
        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

        self.draw_graph()

    def initialize_graph(self):
        # Initial graph before landslide
        edges = [
            ('A', 'B', 2), ('A', 'C', 5), ('B', 'D', 4), ('B', 'E', 7),
            ('C', 'E', 6), ('D', 'E', 1), ('D', 'F', 3), ('E', 'F', 8)
        ]
        for u, v, weight in edges:
            self.graph.add_edge(u, v, weight)
            self.nx_graph.add_edge(u, v, weight=weight)

    def draw_graph(self, path=None):
        self.ax.clear()
        pos = nx.spring_layout(self.nx_graph)  # Layout for visualization

        # Draw nodes
        nx.draw_networkx_nodes(self.nx_graph, pos, ax=self.ax, node_color='lightblue', node_size=500)

        # Draw edges
        nx.draw_networkx_edges(self.nx_graph, pos, ax=self.ax, edgelist=self.nx_graph.edges(), edge_color='gray')

        # Draw shortest path in a different color
        if path:
            path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
            nx.draw_networkx_edges(self.nx_graph, pos, ax=self.ax, edgelist=path_edges, edge_color='red', width=2.5)

        # Draw labels
        nx.draw_networkx_labels(self.nx_graph, pos, ax=self.ax, font_size=12)
        edge_labels = nx.get_edge_attributes(self.nx_graph, 'weight')
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels=edge_labels, ax=self.ax)

        self.canvas.draw()

    def find_shortest_path(self):
        start = self.start_entry.get().upper()
        end = self.end_entry.get().upper()

        if start not in self.graph.graph or end not in self.graph.graph:
            messagebox.showerror("Error", "Invalid locations.")
            return

        distances, shortest_path = self.graph.dijkstra(start, end)
        path = reconstruct_path(shortest_path, start, end)

        if distances[end] == float('infinity'):
            messagebox.showinfo("Result", f"No path found from {start} to {end}.")
        else:
            path_str = ' -> '.join(path)
            messagebox.showinfo("Result", f"Shortest path from {start} to {end}: {path_str}\nTotal distance: {distances[end]} km")
            self.draw_graph(path)  # Redraw the graph showing the path

    def simulate_landslide(self):
        removed_edges = remove_random_edges(self.graph, 2)  # Randomly remove 2 edges
        for u, v in removed_edges:
            self.nx_graph.remove_edge(u, v)  # Remove edge from visualization
        removed_str = ', '.join([f"{u}↔{v}" for u, v in removed_edges])
        messagebox.showinfo("Landslide", f"Landslide blocked roads: {removed_str}")

        self.draw_graph()  # Redraw graph after simulating landslide


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RescueApp(root)
    root.mainloop()
