"""
Example usage of the saha-belletti package.
"""

import networkx as nx
import saha_belletti

# Create a simple graph
graph = nx.Graph()
graph.add_edges_from([(0, 1), (1, 2), (2, 0)])  # Triangle graph

# Generate a quantum circuit for 3-coloring
circuit = saha_belletti.generate_circuit(graph, colors=3, oracle_type='balanced')

print(f"Generated circuit with {circuit.num_qubits} qubits")
print(f"Circuit depth: {circuit.depth()}")

# Get classical solution for comparison
classical_solutions = saha_belletti.cpu_color_graph(graph, 3)
print(f"Classical solutions found: {len(classical_solutions)}")
print(f"Example solution: {classical_solutions[0] if classical_solutions else 'None'}")
