# ===================================================================
# Circuit Optimization Module - Gate Deduplication
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def gate_equal(gate1, gate2):
    """
    Checks if two quantum gates are equivalent.
    
    Two gates are considered equal if they have the same operation name
    and act on the same qubits.
    
    Args:
        gate1, gate2: Qiskit instruction objects to compare
        
    Returns:
        Boolean indicating if gates are equivalent
    """
    return (gate1.operation.name == gate2.operation.name
            and gate1.qubits == gate2.qubits)


def gate_qubits(qc, gate):
    """
    Gets the qubit indices that a gate acts on.
    
    Args:
        qc: QuantumCircuit containing the gate
        gate: Qiskit instruction object
        
    Returns:
        List of integer qubit indices
    """
    return list(map(lambda q: qc.find_bit(q).index, gate.qubits))


def gate_print(qc, gate):
    """
    Debug function to print gate information.
    
    Args:
        qc: QuantumCircuit containing the gate
        gate: Qiskit instruction object
    """
    print(gate.operation.name, gate_qubits(qc, gate))


def gate_write_qubit(qc, gate):
    """
    Gets the qubit that this gate writes to (modifies).
    
    For most quantum gates, this is the last (highest-indexed) qubit
    in the gate's qubit list (the target qubit).
    
    Args:
        qc: QuantumCircuit containing the gate
        gate: Qiskit instruction object
        
    Returns:
        Integer index of the qubit being written to
    """
    return max(gate_qubits(qc, gate))


def gate_read_qubits(qc, gate):
    """
    Gets the qubits that this gate reads from (control qubits).
    
    For most quantum gates, these are all qubits except the target
    (the one being written to).
    
    Args:
        qc: QuantumCircuit containing the gate  
        gate: Qiskit instruction object
        
    Returns:
        List of integer qubit indices being read from
    """
    qubits = gate_qubits(qc, gate)
    qubits.remove(max(qubits))  # Remove target qubit
    return qubits


def make_lines(qc, num_qubits):
    """
    Creates a data structure to track gate history for each qubit.
    
    This creates "timeline" for each qubit showing the sequence of
    gates that have acted on it.
    
    Args:
        qc: QuantumCircuit being analyzed
        num_qubits: Number of qubits in the circuit
        
    Returns:
        Tuple of (qc, lines) where lines[i] is the gate history for qubit i
    """
    return (qc, [[] for i in range(num_qubits)])


def line_gate(lines_q, q, i):
    """
    Gets the gate at position i in qubit q's timeline.
    
    Args:
        lines_q: Lines data structure from make_lines()
        q: Qubit index
        i: Position in the timeline
        
    Returns:
        Gate object at that position
    """
    qc, lines = lines_q
    return lines[q][i][1]


def line_index(lines_q, q, i):
    """
    Gets the circuit index of the gate at position i in qubit q's timeline.
    
    Args:
        lines_q: Lines data structure from make_lines()
        q: Qubit index
        i: Position in the timeline
        
    Returns:
        Integer circuit index of the gate
    """
    qc, lines = lines_q
    return lines[q][i][0]


def lines_add(lines_q, index, gate):
    """
    Adds a gate to the timeline of all qubits it acts on.
    
    Args:
        lines_q: Lines data structure from make_lines()
        index: Circuit index of the gate
        gate: Gate object to add
    """
    qc, lines = lines_q
    for q in gate_qubits(qc, gate):
        lines[q].append((index, gate))


def lines_remove(lines_q, gate, gate_index):
    """
    Removes a gate from all relevant qubit timelines.
    
    Args:
        lines_q: Lines data structure from make_lines()
        gate: Gate object to remove
        gate_index: Circuit index of the gate to remove
    """
    qc, lines = lines_q
    for q in gate_qubits(qc, gate):
        indexes = list(zip(*lines[q]))[0]  # Extract all circuit indices
        i = indexes.index(gate_index)     # Find position of this gate
        lines[q].pop(i)                   # Remove from timeline


def line_back_till(lines_q, q, circuit_index):
    """
    Iterates backwards through a qubit's timeline from a given circuit index.
    
    Args:
        lines_q: Lines data structure from make_lines()
        q: Qubit index
        circuit_index: Starting circuit index (exclusive)
        
    Yields:
        Tuples of (circuit_index, gate) in reverse chronological order
    """
    qc, lines = lines_q
    for index, gate in reversed(lines[q]):
        if index <= circuit_index:
            break  # Stop when we reach the specified index
        yield index, gate


def empty_line(lines_q, q):
    """
    Checks if a qubit's timeline is empty.
    
    Args:
        lines_q: Lines data structure from make_lines()
        q: Qubit index
        
    Returns:
        Boolean indicating if qubit has no gates in its timeline
    """
    qc, lines = lines_q
    return len(lines[q]) == 0


def line_clean(lines_q, q, circuit_index):
    """
    Checks if a qubit has been written to since a given circuit index.
    
    This is used to determine if it's safe to remove a gate - if the
    qubit has been written to since then, the gate's output may have
    been overwritten.
    
    Args:
        lines_q: Lines data structure from make_lines()
        q: Qubit index to check
        circuit_index: Circuit index to check from
        
    Returns:
        Boolean: True if qubit hasn't been written to since circuit_index
    """
    qc, lines = lines_q
    for index, gate in line_back_till(lines_q, q, circuit_index):
        if gate_write_qubit(qc, gate) == q:
            return False  # Qubit has been written to
    return True  # Qubit hasn't been written to


def get_duplicate(lines_q, gate):
    """
    Checks if a gate duplicates a previous gate and can be removed.
    
    A gate can be removed if:
    1. It's identical to the most recent gate on its target qubit
    2. All its control qubits haven't been modified since that previous gate
    3. It's not a Hadamard gate (special case)
    
    Args:
        lines_q: Lines data structure from make_lines()
        gate: Gate to check for duplication
        
    Returns:
        Tuple of (duplicate_gate, duplicate_index) if duplicate found,
        otherwise (None, None)
    """
    qc, lines = lines_q
    
    # Check if target qubit has any previous gates
    if empty_line(lines_q, gate_write_qubit(qc, gate)):
        return None, None

    # Get the most recent gate on the target qubit
    duplicate_index = line_index(lines_q, gate_write_qubit(qc, gate), -1)
    duplicate_gate = line_gate(lines_q, gate_write_qubit(qc, gate), -1)

    # Check if gates are duplicates and control qubits are clean
    if (
            gate.operation.name != "h"           # Not a Hadamard gate
            and gate_equal(gate, duplicate_gate) # Same gate operation and qubits
            and all(map(lambda q: line_clean(lines_q, q, duplicate_index),
                        gate_read_qubits(qc, gate)))  # Control qubits unchanged
    ):
        return duplicate_gate, duplicate_index
    
    return None, None


def deduplicate(qc):
    """
    Removes duplicate gate pairs from a quantum circuit.
    
    This optimization identifies pairs of identical gates that cancel
    each other out (since most quantum gates are self-inverse) and
    marks them for removal.
    
    The algorithm works by:
    1. Tracking the gate history for each qubit
    2. For each new gate, checking if it duplicates a recent gate
    3. If so, marking both gates for deletion
    4. Rebuilding the circuit without the marked gates
    
    Args:
        qc: QuantumCircuit to optimize
        
    Returns:
        Optimized QuantumCircuit with duplicate gates removed
    """
    # Create gate timeline tracking structure
    lines = make_lines(qc, len(qc.qubits))

    # Process each gate in the circuit
    for index, gate in enumerate(qc.data):
        duplicate_gate, duplicate_index = get_duplicate(lines, gate)
        
        if duplicate_gate is not None:
            # Found a duplicate - mark both gates for deletion
            gate.operation.label = "delenda"           # Mark current gate
            duplicate_gate.operation.label = "delenda" # Mark duplicate gate
            
            # Remove the duplicate from tracking (current gate won't be added)
            lines_remove(lines, duplicate_gate, duplicate_index)
        elif gate.operation.name != "barrier":
            # Not a duplicate and not a barrier - add to tracking
            lines_add(lines, index, gate)

    # Rebuild circuit without marked gates
    qc_opt = QuantumCircuit(QuantumRegister(qc.num_qubits),
                            ClassicalRegister(qc.num_clbits))

    # Copy all non-deleted gates to the new circuit
    for ins in qc.data:
        if ins.operation.label != "delenda":
            # Reconstruct the gate in the new circuit
            # This is simpler than figuring out which arguments
            # ins.operation.__class__() requires
            name = ins.operation.name
            qs = gate_qubits(qc, ins)
            
            # Handle different gate types
            if name == "h":
                qc_opt.h(qs[0])
            elif name == "z":
                qc_opt.z(qs[0])
            elif name == "x":
                qc_opt.x(qs[0])
            elif name == "cx":
                qc_opt.cx(qs[0], qs[1])
            elif name == "ccx":
                qc_opt.ccx(qs[0], qs[1], qs[2])
            elif name == "mcx_gray" or ins.operation.name == "mcx":
                qc_opt.mcx(qs[:-1], qs[-1])  # Control qubits, target qubit

    # Add measurement gates (assuming measurements are on computational basis qubits)
    for i in range(qc.num_clbits):
        qc_opt.measure(i, i)

    return qc_opt
