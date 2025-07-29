# ===================================================================
# Original Oracle Implementation (from the original research paper)
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

from .problem import (n, qn, k, invalid_color, graph,
                     history_add, ancilla_index,
                     invalid_colors, comparator)


def original_init(qc, problem):
    """
    Initializes ancilla qubits for the original oracle implementation.
    
    The original oracle uses one ancilla qubit per node to accumulate
    constraint violations for that node. All are initialized to |1⟩.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
    """
    # Initialize one ancilla qubit per node to |1⟩
    for i in range(n(problem)):
        qc.x(ancilla_index(problem) + i)


def original_qubit_count(problem):
    """
    Calculates the total number of qubits needed for the original oracle.
    
    This implementation follows the structure from the original paper
    with some optimizations applied.
    
    Qubit allocation:
    - n * qn qubits for node colors
    - n qubits for per-node constraint accumulation
    - invalid_colors qubits for invalid color detection
    - 1 qubit for final oracle output
    
    Args:
        problem: Problem instance
        
    Returns:
        Total number of qubits required
    """
    return (n(problem) * qn(problem)        # Node color qubits
            + n(problem)                    # Per-node ancilla qubits
            + invalid_colors(problem)       # Invalid color detection qubits
            + 1)                            # Final oracle output qubit


def original_compose(qc, problem):
    """
    Composes the original oracle circuit.
    
    This implementation follows the structure from the original paper:
    1. Check for invalid colors at each node
    2. Combine invalid color results for each invalid color value
    3. Check edge constraints (adjacent nodes with same color)
    4. Combine edge constraints appropriately
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
        
    Returns:
        List of ancilla qubit indices storing constraint results
    """
    # Phase 1: Check for invalid colors
    # For each invalid color value (k, k+1, ..., 2^qn-1)
    for color in range(k(problem), k(problem) + invalid_colors(problem)):
        # Check each node for this invalid color
        for node in range(n(problem)):
            # Apply invalid color constraint to node's ancilla qubit
            invalid_color(qc, problem,
                          color, node, ancilla_index(problem) + node)
            # Add uncomputation to history
            history_add(problem,
                        lambda problem=problem, color=color, node=node,
                        t=ancilla_index(problem) + node:
                        invalid_color(qc, problem, color, node, t))

        # Combine results: if any node has this invalid color, mark it
        sources = [ancilla_index(problem) + node for node in range(n(problem))]
        target = ancilla_index(problem) + n(problem) + color - k(problem)
        qc.mcx(sources, target)  # Multi-controlled X gate
        
        # Add uncomputation to history
        history_add(problem,
                    lambda sources=sources, target=target:
                    qc.mcx(sources, target))

        # Uncompute the invalid color checks
        for node in reversed(range(n(problem))):
            invalid_color(qc, problem,
                          color, node, ancilla_index(problem) + node)
            history_add(problem,
                        lambda problem=problem, color=color, node=node,
                        t=ancilla_index(problem) + node:
                        invalid_color(qc, problem, color, node, t))

    # Phase 2: Check edge constraints (adjacent nodes with same color)
    l = n(problem) - 1  # Index for combining edge results
    f = 0               # Starting index for edge constraint qubits
    
    # Process edges grouped by first node
    for i in range(0, n(problem) - 1):
        r = f  # Range start for this node's edges
        m = f  # Index for uncomputation
        
        # Check all edges from node i to higher-numbered nodes
        for j in range(i + 1, n(problem)):
            if [i, j] in graph(problem).edges:
                # Apply edge constraint (same color check)
                comparator(qc, problem, i, j, ancilla_index(problem) + r)
                # Add uncomputation to history
                history_add(problem,
                            lambda problem=problem, i=i, j=j,
                            t=ancilla_index(problem) + r:
                            comparator(qc, problem, i, j, t))
                r += 1
        
        # If this node has multiple edges, combine their results
        if r > f + 1:
            # Multi-controlled gate to combine edge constraint results
            sources = [ancilla_index(problem) + edge_idx for edge_idx in range(r)]
            target = ancilla_index(problem) + l
            qc.x(target)  # Initialize target to |1⟩
            qc.mcx(sources, target)  # Flip if any edge constraint violated
            
            # Add uncomputation to history
            history_add(problem, lambda sources=sources, target=target:
                        qc.mcx(sources, target))
            history_add(problem, lambda target=target: qc.x(target))
            
            l -= 1  # Move to next combination qubit
            
            # Uncompute the edge constraints
            for j in reversed(range(i + 1, n(problem))):
                if [i, j] in graph(problem).edges:
                    comparator(qc, problem, i, j, ancilla_index(problem) + m)
                    history_add(problem,
                                lambda problem=problem, i=i, j=j,
                                t=ancilla_index(problem) + m:
                                comparator(qc, problem, i, j, t))
                    m += 1
        elif r == f + 1:
            # Single edge: no combination needed
            f += 1

    # Return all ancilla qubits that store constraint results
    return [ancilla_index(problem) + i
            for i in range(n(problem) + invalid_colors(problem))]


# Original oracle system tuple: (qubit_count_func, init_func, compose_func)
# This tuple is used by the main circuit generation function
original_system = (original_qubit_count, original_init, original_compose)
