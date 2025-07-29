# ===================================================================
# Balanced Oracle Implementation 
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

from math import ceil, sqrt
from .problem import (n, qn, ancilla_index,
                     history_add, problem_comp_num,
                     make_components, component_builder, comp_num,
                     greedy_get_components_window
                     )


def balanced_qubits(values):
    """
    Calculates the number of ancilla qubits needed for a given number of constraints.
    
    The balanced oracle uses a triangular number allocation where the number
    of ancilla qubits grows as approximately sqrt(2 * constraints).
    
    This formula comes from: values = 1 + qubits * (qubits - 1) / 2
    Solving for qubits: qubits = ceil((1 + sqrt(8 * values - 7)) / 2)
    
    Args:
        values: Number of constraint components to handle
        
    Returns:
        Number of ancilla qubits required
    """
    return ceil((1 + sqrt(8 * values - 7)) / 2)


def balanced_values(qubits):
    """
    Calculates the maximum number of constraints that can be handled
    with a given number of ancilla qubits.
    
    Args:
        qubits: Number of available ancilla qubits
        
    Returns:
        Maximum constraint components that can be processed
    """
    return 1 + qubits * (qubits - 1) / 2


def balanced_qubit_count(problem):
    """
    Calculates the total number of qubits needed for the balanced oracle.
    
    The balanced oracle provides a compromise between the simple oracle
    (many qubits, low depth) and minimal oracle (few qubits, high depth).
    
    Qubit allocation:
    - n * qn qubits for node colors
    - balanced_qubits(problem_comp_num) ancilla qubits for constraint evaluation
    - 1 qubit for final oracle output
    
    Args:
        problem: Problem instance
        
    Returns:
        Total number of qubits required
    """
    return (n(problem) * qn(problem)                        # Node color qubits
            + balanced_qubits(problem_comp_num(problem))    # Balanced ancilla allocation
            + 1)                                            # Final oracle output qubit


def balanced_init(qc, problem):
    """
    Initializes ancilla qubits for the balanced oracle.
    
    All ancilla qubits are initialized to |1⟩ so they can be
    flipped to |0⟩ when constraints are violated.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
    """
    # Initialize all balanced ancilla qubits to |1⟩
    for i in range(balanced_qubits(problem_comp_num(problem))):
        qc.x(ancilla_index(problem) + i)


def balanced_compose(qc, problem):
    """
    Composes the balanced oracle circuit.
    
    This implementation processes constraints in multiple rounds, where
    each round can handle an increasing number of constraints in parallel.
    The structure creates a balanced trade-off between circuit depth and width.
    
    The algorithm works by:
    1. Starting with the highest ancilla level
    2. Processing as many constraints as possible at each level
    3. Combining results using multi-controlled gates
    4. Moving to lower levels until all constraints are processed
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
        
    Returns:
        List of ancilla qubit indices storing final results
    """
    # Create organized constraint components
    components = make_components(qc, problem)
    ancillas = balanced_qubits(problem_comp_num(problem))
    outputs = []
    
    # Process constraints level by level (top-down)
    for target_i in range(ancillas-1, 1, -1):
        # Check if we can fit all remaining constraints at this level
        if comp_num(components) <= target_i + 1:
            # Process all remaining constraints directly
            comps = greedy_get_components_window(problem, components,
                                                 comp_num(components))
            for i, component in enumerate(map(component_builder, comps)):
                component(ancilla_index(problem) + i)
                history_add(problem,
                            lambda c=component, t=ancilla_index(problem)+i:
                            c(t))
                outputs.append(ancilla_index(problem) + i)
            break

        # Get constraints for this level (up to target_i components)
        components_target = greedy_get_components_window(problem, components,
                                                         target_i)
        if len(components_target) == 0:
            break  # No more constraints to process

        # Apply constraint components at lower ancilla levels
        for i, component in enumerate(list(map(component_builder,
                                               components_target))):
            component(ancilla_index(problem) + i)
            history_add(problem,
                        lambda c=component, t=ancilla_index(problem) + i: c(t))
        
        # Combine results using multi-controlled gate at target level
        sources = [ancilla_index(problem) + i
                   for i in range(len(components_target))]
        
        # Prepare target ancilla (flip to |0⟩ first)
        qc.x(ancilla_index(problem)+target_i)
        history_add(problem,
                    lambda target=ancilla_index(problem)+target_i:
                    qc.x(target))
        
        # Apply multi-controlled gate (AND of all source qubits)
        qc.mcx(sources, ancilla_index(problem)+target_i)
        history_add(problem,
                    lambda sources=sources,
                    target=ancilla_index(problem)+target_i:
                    qc.mcx(sources, target))
        
        outputs.append(ancilla_index(problem)+target_i)
        
        # Uncompute the constraint components
        for i, component in reversed(list(enumerate(map(component_builder,
                                                        components_target)))):
            component(ancilla_index(problem) + i)
            history_add(problem,
                        lambda c=component, t=ancilla_index(problem) + i: c(t))
    
    # Handle final remaining constraints (should be ≤ 2)
    if comp_num(components) <= 2:
        final_comps = greedy_get_components_window(problem, components, 2)
        for i, c in enumerate(map(component_builder, final_comps)):
            c(ancilla_index(problem) + i)
            outputs.append(ancilla_index(problem) + i)
            history_add(problem, lambda c=c, t=ancilla_index(problem)+i: c(t))
        return outputs
    else:
        # This should not happen if the algorithm is correct
        print(comp_num(components))
        raise Exception("Leftover components after compose"
                        "--qubit count might be wrong")


# Balanced oracle system tuple: (qubit_count_func, init_func, compose_func)
# This tuple is used by the main circuit generation function
balanced_system = (balanced_qubit_count, balanced_init, balanced_compose)
