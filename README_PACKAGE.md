# SAHA-BELLETTI: Quantum K-Coloring Circuit Package

A Python package for generating quantum circuits to solve the graph K-coloring problem using various oracle implementations and Grover's algorithm.

Based on the research paper: "Analyzing, Fixing and Optimizing a Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"

## Features

- **Multiple Oracle Implementations:**
  - Simple Oracle (minimum depth, maximum width)
  - Minimal Oracle (minimum width, maximum depth)
  - Balanced Oracle (balanced depth and width)
  - Original Oracle (from the research paper)

- **Circuit Optimization:** Gate deduplication and circuit optimization utilities

- **Analysis Tools:** Statistical visualization and result analysis

- **Classical Utilities:** Graph generation and classical coloring algorithms for verification

## Installation

### From source:
```bash
git clone <repository-url>
cd saha-belletti
pip install -r requirements.txt
pip install -e .
```

### Dependencies:
- qiskit >= 0.45.0
- qiskit-aer >= 0.12.0
- qiskit-ibm-runtime >= 0.15.0
- networkx >= 3.0
- matplotlib >= 3.5.0
- numpy >= 1.21.0
- scipy >= 1.7.0
- alive-progress >= 3.0.0

## Quick Start

```python
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
```

## Package Structure

```
saha_belletti/
├── __init__.py          # Package initialization and public API
├── core.py              # Main circuit generation functions
├── problem.py           # Core problem representation
├── oracles.py           # Oracle implementations interface
├── simple.py            # Simple oracle implementation
├── minimal.py           # Minimal oracle implementation
├── balanced.py          # Balanced oracle implementation
├── original.py          # Original oracle implementation
├── optimization.py      # Circuit optimization utilities
├── histogram.py         # Visualization and analysis tools
└── utils.py             # Utility functions
```

## Oracle Types

- **`'simple'`**: Minimum depth oracle - fastest execution but uses most qubits
- **`'minimal'`**: Minimum width oracle - uses fewest qubits but has greater depth
- **`'balanced'`**: Balanced oracle - compromise between depth and width
- **`'original'`**: Original implementation from the research paper

## API Reference

### Main Functions

- `generate_circuit(graph, colors, oracle_type='balanced', grover_iterations=-1)`: Generate quantum circuit
- `execute_circuit(circuit, backend='simulator', shots=1024)`: Execute circuit
- `analyze_results(results, graph, colors)`: Analyze results

### Utility Functions

- `cpu_color_graph(graph, k)`: Classical brute-force coloring algorithm
- `gen_graph(nodes, colors)`: Generate random graph with specific chromatic number
- `cheat_graph(n, k)`: Generate graph optimized for Grover's algorithm

## Example Usage

See `example.py` for a complete example of using the package.

## Research Paper

This implementation is based on:
"Analyzing, Fixing and Optimizing a Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"

## License

MIT License (see LICENSE file for details)
