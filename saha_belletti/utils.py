"""
Utility functions for the quantum K-coloring package.

This module provides helper functions for graph generation, classical coloring,
and other utilities used throughout the package.
"""

from math import pi, ceil, log2, floor, sqrt
import networkx as nx


def cpu_color_graph(graph, k, node=0, coloring=[]):
    """
    Classical brute-force algorithm to find all valid K-colorings of a graph.
    
    This function serves as the ground truth for validating quantum results.
    It uses recursive backtracking to enumerate all possible valid colorings
    of the given graph using at most k colors.
    
    Args:
        graph: NetworkX graph object to be colored
        k: Maximum number of colors to use
        node: Current node being colored (used in recursion)
        coloring: Partial coloring built so far (used in recursion)
    
    Returns:
        List of valid colorings, where each coloring is a list of color assignments
    """
    # Base case: if all nodes have been colored, return the complete coloring
    if node == graph.order():
        return [coloring]

    def admissible_colors():
        """
        Returns the set of colors that can be assigned to the current node
        without violating the coloring constraint (no adjacent nodes have same color)
        """
        # Start with all available colors {0, 1, ..., k-1}
        # Remove colors already used by neighbors that have been colored
        return set(range(k)) - set(
            [coloring[i] for i in graph.adj[node] if i < len(coloring)])

    # Recursively try all admissible colors for the current node
    valids = []  # List to accumulate all valid colorings
    for color in admissible_colors():
        # Recursively color the remaining nodes with current node assigned 'color'
        valids += cpu_color_graph(graph, k, node+1, coloring + [color])
    return valids


def gen_graph(nodes, colors, max_tries=100000, p=0.2):
    """
    Generates a random graph with exactly the specified chromatic number.
    
    Uses a trial-and-error approach to generate random graphs until one is found
    that has the desired chromatic number (requires exactly 'colors' colors,
    but cannot be colored with fewer colors).
    
    Args:
        nodes: Number of nodes in the graph
        colors: Desired chromatic number (minimum colors needed)
        max_tries: Maximum attempts before giving up
        p: Edge probability for random graph generation
    
    Returns:
        NetworkX graph with the specified chromatic number
    """
    # Special case: complete graph when nodes equals colors
    if nodes == colors:
        return nx.complete_graph(nodes)
    
    print("p =", p)  # Print edge probability for debugging
    
    # Try generating random graphs until one has the right chromatic number
    for i in range(max_tries):
        # Generate random graph with edge probability p
        g = nx.gnp_random_graph(nodes, p)
        
        # Check if graph meets requirements:
        # 1. Must be connected (all nodes reachable)
        # 2. Cannot be colored with (colors-1) colors  
        # 3. Can be colored with exactly 'colors' colors
        if (
                nx.is_connected(g)
                and len(cpu_color_graph(g, colors - 1)) == 0  # No valid (k-1)-colorings
                and len(cpu_color_graph(g, colors)) != 0      # At least one valid k-coloring
        ):
            return g


def cheat_graph(n, k, amt=20):
    """
    Generates a graph optimized for low Grover iteration count.
    
    Creates multiple random graphs and selects the one requiring the fewest
    Grover iterations (i.e., has the most valid colorings relative to total
    search space).
    
    Args:
        n: Number of nodes
        k: Number of colors  
        amt: Number of candidate graphs to generate
    
    Returns:
        NetworkX graph optimized for Grover's algorithm
    """
    # Generate multiple candidate graphs
    graphs = [gen_graph(n, k) for i in range(amt)]
    
    # Select graph requiring minimum Grover iterations
    # Grover iterations = π/4 * sqrt(total_space / num_solutions)
    return min(graphs,
               key=lambda g: floor(pi/4 * sqrt(2 ** (ceil(log2(k)) * len(g))
                                               / len(cpu_color_graph(g, k)))))


__all__ = [
    'cpu_color_graph',
    'gen_graph', 
    'cheat_graph'
]
