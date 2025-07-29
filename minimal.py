# ===================================================================
# Minimal Oracle Implementation (Minimum Width Oracle)  
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

from math import floor, ceil, log2
from problem import (n, qn, ancilla_index, problem_comp_num,
                     get_greedy_components_list,
                     history_add)


def minimal_init(qc, problem):
    """
    Initializes ancilla qubits for the minimal oracle.
    
    The minimal oracle uses a logarithmic number of ancilla qubits
    and builds constraint results in a tree-like structure.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
    """
    # Initialize the first two ancilla qubits to |1⟩
    # These serve as the base level of the computation tree
    qc.x(ancilla_index(problem))
    qc.x(ancilla_index(problem) + 1)


def minimal_qubit_count(problem):
    """
    Calculates the total number of qubits needed for the minimal oracle.
    
    This implementation uses O(log n) ancilla qubits instead of O(n),
    achieving minimum width at the cost of increased depth.
    
    Qubit allocation:
    - n * qn qubits for node colors
    - ceil(log2(problem_comp_num)) qubits for constraint tree
    - 1 qubit for temporary computation
    - 1 qubit for final oracle output
    
    Args:
        problem: Problem instance
        
    Returns:
        Total number of qubits required
    """
    return (n(problem) * qn(problem)                      # Node color qubits
            + ceil(log2(problem_comp_num(problem))) + 1   # Tree ancilla qubits + temp
            + 1)                                          # Final oracle output qubit


def put(qc, problem, i, components):
    """
    Recursively builds a tree structure for constraint evaluation.
    
    This function implements a binary tree where constraint components
    are combined hierarchically. Level i can handle 2^(i-1) components.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
        i: Current tree level (depth from leaves)
        components: List of constraint components to process
    """
    # Validate input size for this level
    if len(components) != 2 ** max(0, i-1):
        raise Exception("Put at level %d requires %d constraints."
                        " Got %d instead."
                        % (i, 2 ** max(0, i-1), len(components)))

    # Base case: first two levels handle components directly
    if i < 2:  
        target = ancilla_index(problem) + i
        components[0](target)  # Apply constraint to ancilla qubit
        # Add uncomputation to history
        history_add(problem, lambda c=components[0], target=target: c(target))
        return

    # Recursive case: build subtrees and combine results
    end = 0
    intervals = []
    
    # Recursively process subtrees (in reverse order for proper dependency)
    for j in reversed(range(i)):
        start = end
        intervals.append(start)
        end += 2 ** max(0, j - 1)
        put(qc, problem, j, components[start:end])
    
    # Combine results from all subtrees using multi-controlled gate
    sources = [ancilla_index(problem) + r for r in range(i)]
    target = ancilla_index(problem) + i
    qc.mcx(sources, target)  # AND all lower level results
    
    # Add uncomputation to history
    history_add(problem,
                lambda sources=sources, target=target: qc.mcx(sources, target))
    
    # Uncompute subtrees (in forward order)
    end = len(components)
    for j, start in zip(range(i), reversed(intervals)):
        put(qc, problem, j, components[start:end])
        end = start


def setup(qc, problem, components):
    """
    Sets up the constraint evaluation tree for all components.
    
    Divides components into chunks that fit the binary tree structure
    and processes them to generate the final oracle result.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
        components: List of all constraint components
        
    Returns:
        List of output ancilla qubit indices
    """
    output_indexes = []
    values = []  # Number of components per tree level
    indexes = []  # Tree level indices
    
    # Start from the highest possible level
    i = ceil(log2(problem_comp_num(problem)))  # Maximum tree depth needed

    # Determine how to partition components across tree levels
    while sum(values) != len(components):
        chunk = 2 ** max(i-1, 0)  # Capacity of level i
        if chunk <= len(components) - sum(values):
            values.append(chunk)
            indexes.append(i)
        i -= 1

    # Process each chunk at its assigned level
    c_i = 0
    for i, chunk in zip(indexes, values):
        put(qc, problem, i, components[c_i:c_i + chunk])
        c_i += chunk
        output_indexes.append(ancilla_index(problem) + i)
    
    return output_indexes


def minimal_compose(qc, problem):
    """
    Composes the minimal oracle circuit.
    
    This implementation achieves minimum width by using a logarithmic
    number of ancilla qubits, organized in a tree structure.
    
    Args:
        qc: QuantumCircuit to modify  
        problem: Problem instance
        
    Returns:
        List of ancilla qubit indices that store final results
    """
    # Get optimized list of constraint components
    components = get_greedy_components_list(qc, problem)
    
    # Build constraint evaluation tree
    return setup(qc, problem, components)


# Minimal oracle system tuple: (qubit_count_func, init_func, compose_func)
# This tuple is used by the main circuit generation function
minimal_system = (minimal_qubit_count, minimal_init, minimal_compose)


# def setup(qc, problem, components):
#     output_indexes = []
#     end = 0
#     print(len(components))
#     while end != len(components):
#         start = end
#         i = floor(log2(len(components) - start)) + 1
#         end += 2 ** max(0, i - 1)
#         print("putting", end-start, "components at", i)
#         put(qc, problem, i, components[start:end])
#         output_indexes.append(ancilla_index(problem) + i)
#     return output_indexes


# The actual way it should be done (by fixing put)
# def setup(qc, problem, components):
#     output_indexes = []
#     values = []
#     i = 0

#     while sum(values) != len(components):
#         chunk = min(2 ** max(i-1, 0), len(components) - sum(values))
#         values.append(chunk)
#         i += 1

#     c_i = 0
#     for i, chunk in reversed(list(enumerate(values))):
#         put(qc, problem, i, components[c_i:c_i + chunk])
#         c_i += chunk
#         output_indexes.append(ancilla_index(problem) + i)
#     return output_indexes