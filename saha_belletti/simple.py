# ===================================================================
# Simple Oracle Implementation (Minimum Depth Oracle)
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

from .problem import (n, qn,
                     history_add, ancilla_index, problem_comp_num,
                     get_components_list,
                     get_greedy_components_list
                     )


def simple_init(qc, problem):
    """
    Initializes ancilla qubits for the simple oracle.
    
    The simple oracle uses one ancilla qubit per constraint component.
    All ancilla qubits are initialized to |1⟩ so that they can be
    flipped to |0⟩ when constraints are violated.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
    """
    # Initialize all constraint ancilla qubits to |1⟩
    for i in range(problem_comp_num(problem)):
        qc.x(ancilla_index(problem) + i)


def simple_qubit_count(problem):
    """
    Calculates the total number of qubits needed for the simple oracle.
    
    Qubit allocation:
    - n * qn qubits for node colors
    - problem_comp_num(problem) qubits for constraint evaluation
    - 1 qubit for the final oracle output (phase kickback)
    
    Args:
        problem: Problem instance
        
    Returns:
        Total number of qubits required
    """
    return (n(problem) * qn(problem)        # Node color qubits
            + problem_comp_num(problem)     # One ancilla per constraint
            + 1)                            # Final oracle output qubit


def simple_compose(qc, problem):
    """
    Composes the simple oracle circuit.
    
    This implementation achieves minimum depth by using one ancilla qubit
    per constraint. All constraints can be evaluated in parallel, giving
    optimal depth but maximum width.
    
    Args:
        qc: QuantumCircuit to modify
        problem: Problem instance
        
    Returns:
        List of ancilla qubit indices that store constraint results
    """
    # Get optimized list of constraint components for parallel execution
    components = get_greedy_components_list(qc, problem)
    
    # Apply each constraint to its dedicated ancilla qubit
    for i in range(len(components)):
        # Apply constraint component to ancilla qubit
        components[i](ancilla_index(problem) + i)
        
        # Add uncomputation function to history
        history_add(problem,
                    lambda c=components[i], x=ancilla_index(problem)+i: c(x))
    
    # Return list of ancilla qubits storing constraint results
    return [ancilla_index(problem) + i for i in range(len(components))]


# Simple oracle system tuple: (qubit_count_func, init_func, compose_func)
# This tuple is used by the main circuit generation function
simple_system = (simple_qubit_count, simple_init, simple_compose)
