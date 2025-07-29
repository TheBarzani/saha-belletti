"""
Saha-Belletti: Quantum Circuit Generator for K-Coloring Problem

This package implements quantum circuits for solving the graph K-coloring problem
using Grover's algorithm, as described in the research paper:
"Analyzing, Fixing and Optimizing a Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"

The package provides multiple oracle implementations:
- Simple Oracle (minimum depth, maximum width)
- Minimal Oracle (minimum width, maximum depth)  
- Balanced Oracle (balanced depth and width)
- Original Oracle (from the original research paper)

Main entry point is the `generate_circuit` function which creates quantum circuits
for K-coloring problems with the specified oracle implementation.
"""

__version__ = "1.0.0"
__author__ = "Belletti et al. & Ismael Barzani"
__email__ = ""

# Lazy imports to avoid dependency issues
def __getattr__(name):
    if name in ['generate_circuit', 'execute_circuit', 'analyze_results']:
        from .core import generate_circuit, execute_circuit, analyze_results
        return locals()[name]
    elif name in ['simple_system', 'minimal_system', 'balanced_system', 'original_system']:
        from .oracles import simple_system, minimal_system, balanced_system, original_system
        return locals()[name]
    elif name in ['cpu_color_graph', 'gen_graph', 'cheat_graph']:
        from .utils import cpu_color_graph, gen_graph, cheat_graph
        return locals()[name]
    else:
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Make main functions available at package level
__all__ = [
    'generate_circuit',
    'execute_circuit', 
    'analyze_results',
    'simple_system',
    'minimal_system',
    'balanced_system',
    'original_system',
    'cpu_color_graph',
    'gen_graph',
    'cheat_graph'
]
