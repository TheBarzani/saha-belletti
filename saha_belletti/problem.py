# ===================================================================
# Problem representation and quantum circuit building blocks
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

from math import ceil, log2


def make_problem(graph, k):
    """
    Creates a problem instance for the K-coloring problem.
    
    The problem representation consists of:
    - The graph to be colored
    - The number of available colors (k)  
    - A history list for tracking quantum operations (for uncomputation)
    
    Args:
        graph: NetworkX graph object to be colored
        k: Number of available colors
    
    Returns:
        Tuple representing the problem: (graph, k, history)
    """
    return (graph, k, [])  # (graph, colors, operation_history)


def graph(problem):
    """Returns the graph from a problem instance."""
    return problem[0]


def k(problem):
    """Returns the number of colors from a problem instance."""
    return problem[1]


def n(problem):
    """Returns the number of nodes in the graph."""
    return graph(problem).order()


def history(problem):
    """
    Returns the operation history for uncomputation.
    
    The history tracks quantum operations that need to be undone
    after oracle evaluation to restore ancilla qubits to |0⟩.
    """
    return problem[2]


def history_add(problem, c):
    """
    Adds an operation to the history for later uncomputation.
    
    Args:
        problem: Problem instance
        c: Function that when called will undo a quantum operation
    """
    history(problem).append(c)


def qn(problem):
    """
    Returns the number of qubits needed per node.
    
    To represent k colors, we need ceil(log2(k)) qubits per node.
    """
    return ceil(log2(k(problem)))


def decompose(problem):
    """
    Performs uncomputation by executing all operations in reverse order.
    
    This is crucial for Grover's algorithm - after marking solutions,
    we must uncompute the oracle to restore ancilla qubits to |0⟩
    before applying the diffusion operator.
    """
    # Execute operations in reverse order (LIFO - Last In, First Out)
    while history(problem):
        history(problem).pop()()  # Pop and execute the uncomputation function


def node_qubits(problem, i):
    """
    Returns the list of qubit indices assigned to node i.
    
    Each node uses qn(problem) consecutive qubits to represent its color.
    
    Args:
        problem: Problem instance
        i: Node index
    
    Returns:
        List of qubit indices for node i
    """
    return list(range(qn(problem)*i, qn(problem)*(i+1)))


def ancilla_index(problem):
    """
    Returns the index where ancilla qubits begin.
    
    Node qubits come first (n * qn qubits), then ancilla qubits.
    """
    return n(problem) * qn(problem)


def invalid_colors(problem):
    """
    Returns the number of invalid color encodings.
    
    With qn qubits per node, we can represent 2^qn values, but only
    k of them correspond to valid colors. The remaining are invalid.
    """
    return 2 ** qn(problem) - k(problem)


def problem_comp_num(problem):
    """
    Returns the total number of constraint components in the oracle.
    
    Each node contributes invalid_colors(problem) constraints (one per invalid color).
    Each edge contributes 1 constraint (adjacent nodes can't have same color).
    """
    return (invalid_colors(problem) * n(problem)  # Invalid color constraints
            + len(graph(problem).edges))           # Edge constraints


def comparator(qc, problem, i, j, f):
    """
    Quantum circuit that checks if two adjacent nodes have the same color.
    
    This implements a constraint that adjacent nodes i and j cannot have
    the same color. The result is stored in ancilla qubit f.
    
    The circuit works by:
    1. XOR node i's color into node j's qubits  
    2. Flip all bits in node j (so |00...0⟩ becomes |11...1⟩)
    3. Multi-controlled NOT with node j controlling f
    4. Undo steps 2 and 1 to restore original state
    
    Args:
        qc: QuantumCircuit to add gates to
        problem: Problem instance
        i, j: Node indices to compare (order doesn't matter)
        f: Target ancilla qubit index
    """
    # Ensure consistent ordering for reproducibility
    if i > j:
        i, j = j, i
    
    # Get qubit indices for both nodes
    a = node_qubits(problem, i)
    b = node_qubits(problem, j)
    
    # Step 1: XOR node i's color into node j's qubits
    for i_qubit, j_qubit in zip(a, b):
        qc.cx(i_qubit, j_qubit)  # CNOT: j = j ⊕ i
        qc.x(j_qubit)            # Flip j qubit
    
    # Step 2: Multi-controlled NOT (if all b qubits are |1⟩, flip f)
    # This triggers when i and j have the same color (after XOR and flip)
    qc.mcx(b, f)
    
    # Step 3: Undo the computation to restore original state
    for i_qubit, j_qubit in reversed(list(zip(a, b))):
        qc.x(j_qubit)            # Undo flip
        qc.cx(i_qubit, j_qubit)  # Undo XOR


def invalid_color(qc, problem, color, i, dest):
    """
    Quantum circuit that checks if node i has an invalid color encoding.
    
    Marks the destination qubit if node i is assigned a color >= k(problem).
    Since we use qn qubits to represent colors, values k, k+1, ..., 2^qn-1
    are invalid.
    
    Args:
        qc: QuantumCircuit to add gates to
        problem: Problem instance  
        color: The invalid color value to check for
        i: Node index to check
        dest: Target ancilla qubit index
    """
    a = node_qubits(problem, i)  # Qubits representing node i's color
    
    # Convert color to binary and determine which qubits should be flipped
    # x_gates[j] = True means qubit j should be 0 for this color
    x_gates = [not bool(int(x)) for x in bin(color)[2:]]
    qnum = len(x_gates)
    
    # Flip qubits that should be 0 for this color
    for j in range(qnum):
        if x_gates[j]:
            qc.x(a[0] + j)
    
    # Multi-controlled NOT: if all qubits match the pattern, flip dest
    qc.mcx(a, dest)
    
    # Undo the flips to restore original state
    for j in range(qnum):
        if x_gates[j]:
            qc.x(a[0] + j)


def diffusion(qc, problem):
    """
    Implements the diffusion operator (inversion about average) for Grover's algorithm.
    
    This is the amplitude amplification step that increases the amplitude of
    marked states (valid colorings) and decreases the amplitude of unmarked
    states (invalid colorings).
    
    The diffusion operator applies:
    1. Hadamard on all node qubits
    2. X gates on all node qubits  
    3. Multi-controlled Z gate
    4. Undo X gates
    5. Undo Hadamard gates
    
    Args:
        qc: QuantumCircuit to add gates to
        problem: Problem instance
    """
    # Apply to all qubits representing node colors
    node_qubit_count = ancilla_index(problem) - 1
    
    # Step 1: Hadamard all node qubits (transform to computational basis)
    for i in range(node_qubit_count):
        qc.h(i)
        qc.x(i)  # Also apply X gate
    
    # Step 2: Apply phase flip to |00...0⟩ state  
    qc.z(ancilla_index(problem) - 1)  # Single qubit Z gate
    qc.mcx(list(range(node_qubit_count)), ancilla_index(problem) - 1)  # Multi-controlled X
    qc.z(ancilla_index(problem) - 1)  # Another Z gate
    
    # Step 3: Undo the X and Hadamard gates
    for i in range(node_qubit_count):
        qc.x(i)  # Undo X gate
        qc.h(i)  # Undo Hadamard gate


def get_components_list(qc, problem):
    """
    Creates a flat list of all constraint components for the simple oracle.
    
    This is used by the simple (minimum depth) oracle implementation that
    uses one ancilla qubit per constraint component.
    
    Returns functions that when called with an ancilla qubit index will
    add the appropriate constraint checking circuit.
    
    Args:
        qc: QuantumCircuit to add gates to
        problem: Problem instance
        
    Returns:
        List of component functions
    """
    components = []
    
    # Add invalid color components for each node and invalid color
    for color in range(k(problem), 2 ** qn(problem)):  # Invalid colors only
        for i in range(n(problem)):  # Each node
            components.append(
                lambda x, i=i, color=color:
                invalid_color(qc, problem, color, i, x))
    
    # Add edge constraint components
    for i, j in graph(problem).edges:
        components.append(
            lambda x, i=i, j=j:
            comparator(qc, problem, i, j, x))
    
    return components


def make_components(qc, problem):
    """
    Creates organized constraint components for optimized oracle implementations.
    
    Organizes constraints by node to enable parallel execution and minimize
    circuit depth. Returns separate structures for edge and color constraints.
    
    Args:
        qc: QuantumCircuit to add gates to  
        problem: Problem instance
        
    Returns:
        Tuple of (arcs, colors) where:
        - arcs[i] = list of edge constraints involving node i
        - colors[i] = list of invalid color constraints for node i
    """
    # Get the graph and create a mapping from node labels to indices
    g = graph(problem)
    node_list = list(g.nodes())
    node_to_index = {node: idx for idx, node in enumerate(node_list)}
    
    # Initialize arc constraints organized by node index
    arcs = [[] for i in range(n(problem))]
    
    # Populate arc constraints (each edge appears in both incident nodes' lists)
    for i, j in g.edges:
        # Convert node labels to indices
        i_idx = node_to_index[i]
        j_idx = node_to_index[j]
        
        def c(x, i_orig=i_idx, j_orig=j_idx):
            return comparator(qc, problem, i_orig, j_orig, x)
        
        # Add constraint to both nodes' lists (with edge identifier)
        arcs[i_idx].append(((i_idx, j_idx), c))
        arcs[j_idx].append(((i_idx, j_idx), c))

    # Create invalid color constraints organized by node
    colors = [[((i,),  # Node identifier (tuple for consistency)
                lambda x, i=i, color=color:
                invalid_color(qc, problem, color, i, x))
               for color in range(k(problem), 2 ** qn(problem))]  # Invalid colors
              for i in range(n(problem))]  # Each node
    
    return arcs, colors


def arcs_comp(components):
    """Returns the arc constraints from organized components."""
    return components[0]


def colors_comp(components):
    """Returns the color constraints from organized components."""  
    return components[1]


def node_arcs_comp(components, i):
    """Returns arc constraints for node i."""
    return arcs_comp(components)[i]


def node_colors_comp(components, i):
    """Returns color constraints for node i."""
    return colors_comp(components)[i]


def component_nodes(component):
    """Returns the node(s) involved in a constraint component."""
    return component[0]


def component_builder(component):
    """Returns the function that builds the constraint circuit."""
    return component[1]


def is_arc(component):
    """Checks if a component is an edge constraint (vs. color constraint)."""
    return len(component_nodes(component)) == 2


def comp_num(components):
    """
    Returns the total number of constraint components.
    
    Counts color constraints plus unique edge constraints (each edge
    appears in two nodes' lists but should only be counted once).
    """
    color_count = sum(1
                     for node_color_comps in colors_comp(components)
                     for i in node_color_comps)
    
    arc_count = int(sum(1
                       for node_arcs_comps in arcs_comp(components)
                       for i in node_arcs_comps) / 2)  # Divide by 2 since each edge counted twice
    
    return (color_count + arc_count)


def remove_component(components, component):
    """
    Removes a constraint component from the organized structure.
    
    Used during greedy component selection to avoid double-counting.
    
    Args:
        components: Organized component structure
        component: Component to remove
    """
    for i in component_nodes(component):
        if is_arc(component):
            node_arcs_comp(components, i).remove(component)
        else:
            node_colors_comp(components, i).remove(component)


def greedy_get_components_window(problem, components, amount):
    """
    Greedily selects constraint components for parallel execution.
    
    This function implements a greedy algorithm to select up to 'amount'
    constraint components that can be executed in parallel (no two
    components share the same node).
    
    The algorithm prioritizes nodes with the most remaining constraints
    to achieve better load balancing.
    
    Args:
        problem: Problem instance
        components: Organized component structure (modified in-place)
        amount: Maximum number of components to select
        
    Returns:
        List of selected constraint components
    """
    def ranking():
        """
        Returns nodes sorted by number of remaining arc constraints (descending).
        
        Prioritizing nodes with more constraints helps achieve better
        parallel execution and load balancing.
        """
        return sorted(range(n(problem)),
                      key=lambda x: -len(node_arcs_comp(components, x)))

    def next_component(nodes):
        """
        Selects the next component from available nodes.
        
        Prioritizes arc constraints over color constraints when possible,
        as arc constraints are typically more expensive to compute.
        
        Args:
            nodes: List of available nodes (not yet used in this window)
            
        Returns:
            Next component to add, or None if no components available
        """
        for node in nodes:
            # First try to find an arc constraint with both endpoints available
            for arc in node_arcs_comp(components, node):
                one, other = component_nodes(arc)
                if one in nodes and other in nodes:
                    return arc
            
            # If no arc constraints available, try color constraints
            if len(node_colors_comp(components, node)):
                return node_colors_comp(components, node)[-1]  # Take last color constraint

    window = []  # Selected components for parallel execution
    
    # Keep selecting components until we have enough or run out
    while len(window) < amount and comp_num(components) != 0:
        # Gather fully-parallelized lists of components until we have
        # "amount" components in total
        nodes = ranking()  # Prioritize nodes with most remaining constraints
        
        while len(window) < amount:
            # Choose as many components as possible to run in parallel
            chosen_component = next_component(nodes)
            if chosen_component is None:
                break  # No more components available with current nodes
                
            window.append(chosen_component)                    # Add to selection
            remove_component(components, chosen_component)     # Remove from future consideration
            
            # Remove nodes involved in this component from available nodes
            for i in component_nodes(chosen_component):
                nodes.remove(i)
                
    return window


def get_greedy_components_list(qc, problem):
    """
    Creates an optimized list of constraint components using greedy selection.
    
    This function is used by oracle implementations that want to optimize
    for parallel execution. It organizes all constraints into groups that
    can be executed in parallel, minimizing circuit depth.
    
    Args:
        qc: QuantumCircuit to add gates to
        problem: Problem instance
        
    Returns:
        List of component builder functions in optimized order
    """
    # Create organized component structure
    components = make_components(qc, problem)
    
    # Greedily select all components for optimal parallel execution
    comp_list = greedy_get_components_window(problem,
                                             components,
                                             comp_num(components))
    
    # Extract the component builder functions
    return list(map(component_builder, comp_list))
