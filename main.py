# ===================================================================
# Main module for quantum circuit generation for the K-coloring problem
# Part of the research paper: "Analyzing, Fixing and Optimizing a 
# Space-Efficient Quantum Circuit for the Graph K-Coloring Problem"
# ===================================================================

# Standard library imports for mathematical operations
from math import sqrt, pi, ceil, log2, floor  # Mathematical functions for calculations
from statistics import fmean  # Statistical mean function

# Configuration file parsing
import configparser  # For reading configuration from config.ini

# Graph theory and visualization
import networkx as nx  # Graph theory library for creating and manipulating graphs
import matplotlib.pyplot as plt  # Plotting library for visualizations

# Qiskit imports for quantum computing
from qiskit_ibm_runtime import QiskitRuntimeService  # IBM Quantum runtime service
from qiskit_ibm_runtime import SamplerV2 as Sampler  # Quantum sampler for execution
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager  # Circuit optimization
from qiskit import (QuantumCircuit, QuantumRegister, ClassicalRegister)  # Quantum circuit components
from qiskit.visualization import plot_histogram  # Histogram plotting for quantum results
from qiskit_aer.noise import NoiseModel  # Noise modeling for realistic simulations
from qiskit_aer import AerSimulator  # Local quantum simulator

# QASM (Quantum Assembly) import/export
from qiskit.qasm3 import dump, dumps  # For exporting circuits to QASM format

# Utility imports
import pickle  # For serializing/deserializing Python objects
from alive_progress import alive_bar  # Progress bar for long-running operations
from time import strftime  # Time formatting for log files

# Local module imports - core problem implementation
from problem import decompose, diffusion, make_problem  # Problem definition and operations
from optimization import deduplicate  # Circuit optimization routines

# Local module imports - different oracle implementations
from simple import simple_system  # Minimum depth oracle implementation
from minimal import minimal_system  # Minimum width oracle implementation  
from balanced import balanced_system  # Balanced oracle implementation
from original import original_system  # Original paper oracle implementation

# Visualization utilities
from histogram import plot_simulation_data  # Custom histogram plotting for simulation results



def make_circuit(graph, color_number, method, data, grover_iterations=-1):
    """
    Constructs a quantum circuit for the K-coloring problem using Grover's algorithm.
    
    This function is the core of the quantum circuit generation process. It creates
    a quantum circuit that can solve the graph K-coloring problem using one of the
    implemented oracle methods (minimum depth, minimum width, balanced, or original).
    
    Args:
        graph: NetworkX graph object representing the graph to be colored
        color_number: Number of colors (k) available for coloring
        method: Tuple containing (qubit_count_func, init_func, compose_func) 
                for the chosen oracle implementation
        data: Dictionary to store circuit metadata and results
        grover_iterations: Number of Grover iterations to perform (-1 for optimal)
    
    Returns:
        QuantumCircuit: The constructed quantum circuit ready for execution
    """
    # Extract the three functions from the method tuple
    qubit_count, init, compose = method

    # Graph parameters
    n = graph.order()  # Number of nodes in the graph
    k = color_number   # Number of available colors
    qn = ceil(log2(k))  # Number of qubits needed per node to represent k colors

    # Calculate optimal Grover iterations if not specified
    if grover_iterations == -1:
        # Total number of possible colorings (all combinations)
        all_colorings = 2 ** (qn * len(conf["graph"]))
        # Number of valid colorings (solutions to the problem)
        correct_colors = len(cpu_color_graph(conf["graph"], conf["k"]))

        # Grover's optimal iteration formula: π/4 * sqrt(N/M)
        # where N is total search space and M is number of solutions
        grover_iterations = floor(pi/4 * sqrt(all_colorings / correct_colors))
    
    # Store the calculated iterations in data for analysis
    data["grover_iterations"] = grover_iterations
    print("Grover iterations:", grover_iterations)
    # inv_col = 2 ** qn - k  # Number of invalid colors (commented out)

    def node_qubits(i):
        """Returns the list of qubit indices assigned to node i"""
        return list(range(qn*i, qn*(i+1)))

    # Create the problem representation
    problem = make_problem(graph, k)

    # Calculate total number of qubits needed (depends on oracle implementation)
    num_qubits = qubit_count(problem)

    # Create the quantum circuit with quantum and classical registers
    qc = QuantumCircuit(QuantumRegister(num_qubits),
                        ClassicalRegister(n * qn, name="creg"))

    # Initialize superposition state on all node qubits
    # This creates an equal superposition of all possible colorings
    for i in range(qn*n):
        qc.h(i)  # Hadamard gate creates superposition

    # Initialize the ancilla qubit for phase kickback in Grover's algorithm
    qc.x(num_qubits - 1)  # Set ancilla to |1⟩
    qc.h(num_qubits - 1)  # Put ancilla in |−⟩ state for phase kickback

    # Initialize oracle-specific ancilla qubits
    init(qc, problem)

    # Grover iteration loop
    for i_grv in range(grover_iterations):
        # Create fresh problem instance for each iteration (clears history)
        problem = make_problem(graph, k)  # new history
        
        # Apply the oracle (marks invalid colorings)
        qv = compose(qc, problem)  # Get list of oracle output qubits
        qc.mcx(qv, num_qubits - 1)  # Multi-controlled X gate for phase kickback
        
        # Undo oracle computation (uncompute)
        decompose(problem)
        
        # Apply diffusion operator (amplitude amplification)
        diffusion(qc, problem)

    # Measure all node qubits to read out the final coloring
    for i in range(qn*n):
        qc.measure(i, i)

    return qc


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


def configure(args_kw, data):
    """
    Configures the system by reading config.ini and applying command-line overrides.
    
    This function handles all configuration parsing, type conversion, and default
    value assignment. It merges settings from the configuration file with any
    parameters passed as keyword arguments to main().
    
    Args:
        args_kw: Dictionary of keyword arguments passed to main()
        data: Dictionary to store configuration metadata
    
    Returns:
        Dictionary containing the complete configuration for the current run
    """
    # Read the configuration file
    config_f = configparser.ConfigParser()
    config_f.read("config.ini")

    def parse(v):
        """
        Intelligently parse configuration values from strings to appropriate types.
        Handles booleans, integers, floats, and strings.
        """
        # Boolean parsing (case-insensitive)
        if v.lower() in ["yes", "true", "on"]:
            return True
        if v.lower() in ["no", "false", "off"]:
            return False
        
        # Try integer parsing
        try:
            return int(v)
        except ValueError:
            pass
        
        # Try float parsing  
        try:
            return float(v)
        except ValueError:
            pass
        
        # Default to string
        return v

    # Build configuration dictionary
    conf = {}
    
    # Load graph configuration section
    conf.update([(key, parse(value))
                 for key, value in config_f["graph"].items()])
    
    # Load options configuration section
    conf.update([(key, parse(value))
                 for key, value in config_f["options"].items()])
    
    # Apply command-line overrides (only non-None values)
    conf.update([(key, value)
                 for key, value in args_kw.items()
                 if value is not None])

    # Set derived configuration values
    if "figsize" not in conf:
        # Create figure size tuple from individual width/height settings
        conf["figsize"] = (conf["histogram_size_w"], conf["histogram_size_h"])
    
    # Generate graph if not provided explicitly
    if "graph" not in conf:
        if conf["generate"] == "complete":
            # Generate complete graph (every node connected to every other node)
            conf["graph"] = nx.complete_graph(conf["k"])
            print("Generating complete graph of", conf["k"], "colors")
        elif conf["generate"] == "random":
            # Generate random graph with specified chromatic number
            conf["graph"] = gen_graph(
                conf.get("nodes", conf["k"]),  # Default nodes = k if not specified
                conf["k"])
            print("Generating random graph with", conf["nodes"],
                  "nodes with chromatic number:", conf["k"])

    # Map system names to implementation functions
    systems = {"simple": simple_system,      # Minimum depth oracle
               "minimal": minimal_system,    # Minimum width oracle  
               "balanced": balanced_system,  # Balanced oracle
               "original": original_system}  # Original paper oracle

    # Store system name for logging, then replace with function tuple
    data["system"] = conf["system"]
    conf["system"] = systems[conf["system"]]
    
    return conf


def run_circ(qc, conf, data):
    """
    Executes the quantum circuit using the specified backend (local, online, or quantum hardware).
    
    This function handles three execution modes:
    1. Local simulation (with optional noise models)
    2. Online IBM Quantum simulator 
    3. Real quantum hardware execution
    
    Args:
        qc: QuantumCircuit to execute
        conf: Configuration dictionary specifying execution parameters
        data: Dictionary to store execution results and metadata
    
    Returns:
        Dictionary containing measurement counts from circuit execution
    """
    global results  # Global variable to store detailed results
    
    if conf["run"] == "local":  # Local simulation mode
        if conf["quantum_sim"]:
            # Use noise model from specified IBM backend
            data["noise_model"] = conf["quantum_sim"]
            print("Noise model:", conf["quantum_sim"])
            
            # Get the real backend to extract its noise characteristics
            service = QiskitRuntimeService()
            qbackend = service.get_backend(conf["quantum_sim"])
            noise_model = NoiseModel.from_backend(qbackend)
            
            # Create local simulator with noise model
            backend = AerSimulator(noise_model=noise_model)
        else:
            # Noiseless local simulation
            backend = AerSimulator()
        
        print("Simulating circuit locally")
        job = backend.run(qc)  # Execute the circuit
        results = job.result()  # Get detailed results
        data["results"] = results
        return results.get_counts()  # Return measurement counts
        
    elif conf["run"] == "online" or conf["run"] == "quantum":
        # IBM Quantum service execution (online simulator or real hardware)
        service = QiskitRuntimeService()
        
        if conf["run"] == "online":
            # Online simulator execution
            print("Simulating circuit on online servers")
            backend = service.get_backend(conf["online_sim"])
            shots = conf["online_shots"]  # Number of measurement shots
        else:
            # Real quantum hardware execution
            qp = conf["quantum_sim"]  # Quantum processor name
            if not qp:
                # Auto-select least busy quantum processor with sufficient qubits
                qpc = service.least_busy(simulator=False,
                                         min_num_qubits=qc.num_qubits)
                qp = qpc.name
            print("Running on quantum computer", qp)
            data["quantum_sim"] = qp
            backend = service.get_backend(qp)
            shots = conf["quantum_shots"]  # Number of measurement shots
        
        # Transpile circuit for the target backend (optimization and mapping)
        pass_manager = generate_preset_pass_manager(optimization_level=3,
                                                    backend=backend)
        transpiled = pass_manager.run(qc)
        data["transpiled"] = transpiled  # Store transpiled circuit for analysis
        
        # Execute using the Sampler primitive
        sampler = Sampler(backend)
        job = sampler.run([transpiled], shots=shots)
        results = job.result()[0]  # Get results from first (and only) circuit
        data["results"] = results.data.creg  # Store measurement data
        return results.data.creg.get_counts()  # Return measurement counts
    else:
        # Don't execute - just return circuit for analysis
        print("Not executing the circuit")
        return None


def plot_graph(graph):
    """
    Visualizes a NetworkX graph using matplotlib.
    
    Args:
        graph: NetworkX graph object to visualize
    """
    p = nx.draw(graph)  # Draw the graph
    plt.show()          # Display the plot
    plt.close(p)        # Clean up resources


def plot_figures(measures, figsize):
    """
    Creates and saves a histogram of measurement results.
    
    Args:
        measures: Dictionary of measurement counts from quantum execution
        figsize: Tuple specifying figure dimensions (width, height)
    """
    # Create histogram plot of quantum measurement results
    fig = plot_histogram(measures, figsize=figsize)
    fig.tight_layout()                    # Adjust layout for better appearance
    fig.savefig("measures_new.png")       # Save to file
    # plt.show()                          # Commented out - don't display interactively
    plt.close(fig)                        # Clean up resources


def plot_circuit(qc):
    """
    Visualizes a quantum circuit using matplotlib.
    
    Args:
        qc: QuantumCircuit object to visualize
    """
    p = qc.draw(output="mpl")  # Draw circuit as matplotlib figure
    plt.show()                 # Display the plot
    plt.close(p)               # Clean up resources


# Global list to store graphs used across multiple experiments
graphs = []


def main(k=None, graph=None, run=None, grover_iterations=None,
         online_sim=None, quantum_sim=None, local_shots=None,
         online_shots=None, quantum_shots=None, print_circuit=None,
         figsize=None, generate=None, nodes=None, print_graph=None,
         system=None, deduplicate_opt=None):
    kwargs = locals().copy()  # keyword arguments as a dict

    global conf, measures
    data = {}
    conf = configure(kwargs, data)

    graphs.append(conf["graph"])

    drawings = []

    if conf["print_graph"]:
        drawings.append(lambda: plot_graph(conf["graph"]))

    data["graph"] = nx.from_edgelist(conf["graph"].edges())
    print(conf["graph"].edges())
    qc = make_circuit(conf["graph"], conf["k"],
                      conf["system"], data,
                      conf["grover_iterations"])

    data["circuit"] = qc
    data["depth"] = qc.depth()
    data["width"] = qc.num_qubits

    print("depth:", qc.depth())
    print("width:", qc.num_qubits)
    # qc.draw(output="mpl")
    if conf["deduplicate_opt"]:
        print("Deduplicating gates...")
        qc = deduplicate(qc)
        data["opt_depth"] = qc.depth()
        print("  After optimization:")
        print("depth:", qc.depth())
        print("width:", qc.num_qubits)
    data["dxw"] = qc.depth() * qc.num_qubits
    print(" -> depth * width:", qc.depth() * qc.num_qubits)
    if print_circuit:
        drawings.append(lambda: plot_circuit(qc))

    measures = run_circ(qc, conf, data)

    if measures is None:
        while drawings:
            drawings.pop()()
        return data

    plot_figures(measures, conf["figsize"])

    n = conf["graph"].order()
    qn = ceil(log2(conf["k"]))

    (all_colorings, correct_colors, measures_of_correct,
     measures_of_incorrect) = interpret_measures(conf, measures)

    data["cpu_sol_num"] = correct_colors
    data["colorings_num"] = all_colorings
    print("Number of solutions(cpu):", correct_colors,
          "/", all_colorings)
    if correct_colors != 0:
        data["opt_grover"] = pi / 4 * sqrt(all_colorings / correct_colors)
        data["random_guess_chance"] = correct_colors / all_colorings
        data["correct_chance"] = (sum(measures_of_correct)
                                  / sum(measures.values()))
        data["avg_prob_corr"] = (fmean(measures_of_correct)
                                 / sum(measures.values()))
        data["avg_prob_inc"] = (fmean(measures_of_incorrect)
                                / sum(measures.values()))
        print("Optimal grover iterations number:",
              pi / 4 * sqrt(all_colorings / correct_colors))
        print("Random guess chance of being correct:",
              correct_colors / all_colorings)
        print("Chance of getting a correct result:",
              sum(measures_of_correct)/sum(measures.values()))
        print("Average \"probability\" of individual correct outcomes:",
              fmean(measures_of_correct)/sum(measures.values()))
        print("Average \"probability\" of individual incorrect outcomes:",
              fmean(measures_of_incorrect)/sum(measures.values()))

    while drawings:
        drawings.pop()()
    return data


def interpret_measures(conf, measures):
    qn = ceil(log2(conf["k"]))
    all_colorings = 2 ** (qn * len(conf["graph"]))
    correct_colors = cpu_color_graph(conf["graph"], conf["k"])

    def coloring(code):  # parse the measured colors into ints
        for i in reversed(list(range(int(len(code)/qn)))):
            yield int("".join(reversed(code[i*qn:(i+1)*qn])), 2)

    measures_of_correct = []
    measures_of_incorrect = []

    for code, count in measures.items():
        if list(coloring(code)) in correct_colors:
            measures_of_correct.append(count)
        else:
            measures_of_incorrect.append(count)

    for i in range(len(correct_colors) - len(measures_of_correct)):
        measures_of_correct.append(0)

    for i in range(2 ** (qn * len(conf["graph"]))
                   - len(correct_colors) - len(measures_of_incorrect)):
        measures_of_incorrect.append(0)

    return (all_colorings, len(correct_colors),
            measures_of_correct, measures_of_incorrect)


# generate graph with specific chromatic number
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


def backends():
    """
    Returns a list of available IBM Quantum backends.
    
    Returns:
        List of backend names available through IBM Quantum service
    """
    service = QiskitRuntimeService()
    return list(map(lambda x: x.name(), service.backends()))


def simulation(graph, k, iterations=5):
    """
    Runs comprehensive simulation experiments across multiple systems and noise models.
    
    This function performs batch experiments testing all four oracle implementations
    (simple, minimal, balanced, original) against multiple IBM quantum device noise
    models. Results are logged to a pickle file for later analysis.
    
    Args:
        graph: NetworkX graph to test
        k: Number of colors to use
        iterations: Number of repetitions per system-noise combination
    """
    # Create timestamped log file
    with open("log" + strftime("%Y_%m_%d__%H_%M") + ".pkl", "wb") as logfile:
        # Progress bar for total number of experiments (4 systems × 4 noise models × iterations)
        with alive_bar(4 * 4 * iterations) as bar:
            # Test each oracle implementation
            for system in ["simple", "minimal", "balanced", "original"]:
                # Test each IBM quantum device noise model
                for noise_model in ['ibm_sherbrooke', 'ibm_brisbane',
                                    'ibm_kyoto', 'ibm_osaka']:
                    # Repeat each combination for statistical significance
                    for _ in range(iterations):
                        # Run experiment with current configuration
                        data = main(graph=graph, k=k,
                                    system=system,
                                    quantum_sim=noise_model)
                        bar()                    # Update progress bar
                        pickle.dump(data, logfile)  # Save results to log file
                        logfile.flush()          # Ensure data is written to disk


class Dummy:
    """Placeholder class for handling unpickling errors."""
    pass

class UnpicklerIgnoreErrors(pickle._Unpickler):
    """
    Custom unpickler that handles missing classes gracefully.
    
    When loading pickled data, some Qiskit classes may not be available
    in the current environment. This unpickler replaces them with dummy
    objects to allow analysis of the remaining data.
    """
    def find_class(self, module, name):
        try:
            # Replace problematic Qiskit classes with dummy objects
            if (name == "CircuitInstruction" or name == "QuantumCircuit"):
                return Dummy
            return super().find_class(module, name)
        except AttributeError:
            return Dummy
    

def loadlog(filename="log.pkl"):
    """
    Loads experimental data from a pickle log file.
    
    Uses the custom UnpicklerIgnoreErrors to handle missing Qiskit classes
    gracefully. Continues reading until end of file is reached.
    
    Args:
        filename: Path to the pickle log file
    
    Returns:
        List of experimental data dictionaries
    """
    objects = []
    with open(filename, "rb") as logfile:
        unpk = UnpicklerIgnoreErrors(logfile)  # Use custom unpickler
        while True:
            try:
                objects.append(pickle.load(logfile))  # Load next object
            except EOFError:
                break  # End of file reached
    return objects


def format_data(results):
    """
    Formats experimental results for statistical analysis and plotting.
    
    Organizes results by noise model and system type, extracting the
    'correct_chance' metric for each experiment.
    
    Args:
        results: List of experimental data dictionaries from loadlog()
    
    Returns:
        Nested dictionary: {noise_model: {system: [correct_chances]}}
    """
    # Define the noise models tested
    noise_models = ['ibm_sherbrooke', 'ibm_brisbane',
                    'ibm_kyoto', 'ibm_osaka']
    
    # Initialize nested dictionary structure
    dic = {x: {} for x in noise_models}
    for system in ["simple", "minimal", "balanced", "original"]:
        for noise_model in noise_models:
            dic[noise_model][system] = []
    
    # Extract correct_chance values and organize by noise model and system
    for o in results:
        dic[o["noise_model"]][o["system"]].append(o["correct_chance"])
    
    return dic


def plot_simulation(filename):
    """
    Loads simulation data and creates a comprehensive comparison plot.
    
    Args:
        filename: Path to the pickle log file containing simulation results
    """
    sim = loadlog(filename)                    # Load experimental data
    data = format_data(sim)                    # Format for plotting
    random_guess_chance = sim[0]["random_guess_chance"]  # Baseline probability
    plot_simulation_data(data, random_guess_chance)     # Create visualization


def simulation_details(filename, k):
    """
    Extracts detailed complexity metrics from simulation results.
    
    Analyzes the first result from each system to extract circuit complexity
    metrics including width, depth, depth×width, and ancilla qubit count.
    
    Args:
        filename: Path to the pickle log file
        k: Number of colors (needed for ancilla calculation)
    
    Returns:
        Dictionary with complexity metrics for each system
    """
    sim = loadlog(filename)              # Load experimental data
    n = len(sim[0]["graph"].nodes)       # Number of nodes in the graph
    chunk = int(len(sim)/4)              # Results are grouped by system
    
    data = {}
    # Analyze first result from each system (assuming 4 systems total)
    for i in range(4):
        s = sim[i*chunk]         # Get first result for this system
        system = s["system"]     # System name
        w = s["width"]           # Circuit width (total qubits)
        d = s["depth"]           # Circuit depth (time steps)
        
        # Calculate ancilla qubits: total qubits - node qubits - 1 final ancilla
        anc = s["width"] - ceil(log2(k)) * n - 1
        
        data[system] = {"width": w,
                        "depth": d,
                        "complexity": w * d,  # Depth×width complexity metric
                        "ancillae": anc}      # Number of ancilla qubits
    return data


def qasm2():
    """
    Generates QASM files for all system-size-color combinations.
    
    Creates quantum assembly files for circuits generated by each oracle
    implementation across different graph sizes and color counts. These
    files can be used for external analysis or execution.
    """
    # Map system names to formal names used in filenames
    names = {"simple": "minimum_depth",
             "minimal": "minimum_width", 
             "balanced": "balanced",
             "original": "original"}

    # Progress bar for total number of combinations (4 systems × 6 sizes × 4 colors)
    with alive_bar(4 * 6 * 4) as bar:
        # Test each oracle implementation
        for system in ["simple", "minimal", "balanced", "original"]:
            # Test graph sizes from 3 to 8 nodes
            for n in range(3, 9):
                # Test color counts from 2 to 4  
                for k in range(2, 5):
                    if k > n:  # Skip impossible cases (more colors than nodes)
                        break
                    
                    print("system:", system, "n:", n, "k:", k)
                    
                    # Generate filename and create QASM file
                    filename = ("qasm/" + "example_graph_" + names[system]
                              + "_n" + str(n) + "_k" + str(k) + ".qasm")
                    
                    with open(filename, "w") as f:
                        # Generate circuit and export to QASM format
                        circuit = main(generate="random",
                                      nodes=n, k=k, system=system,
                                      run="")["circuit"]  # Don't execute, just generate
                        dump(circuit, f)  # Export to QASM file
                        bar()             # Update progress bar


def qasm3(log, k):
    """
    Exports circuits from simulation log to QASM files.
    
    Takes experimental results and exports the generated circuits to QASM
    format for external analysis. Typically used for circuits that were
    tested under noise models.
    
    Args:
        log: List of experimental results from loadlog()
        k: Number of colors used in the experiments
    """
    graph = log[0]["graph"]       # Get the graph used in experiments
    n = len(graph.nodes())        # Number of nodes
    
    # Export circuits from specific log entries (assuming specific ordering)
    for i in [0, 20, 40, 60]:    # Select representative experiments
        system = log[i]["system"] # Get system name
        print("system:", system)
        
        # Create filename for this system
        filename = ("qasm/noisy_simulation/" + system
                  + "_n" + str(n) +  "_k" + str(k) + ".qasm")
        
        with open(filename, "w") as f:
            # Regenerate circuit for this configuration
            c = main(graph=graph, k=k, system=system, run="")["circuit"]
            print(c.qasm(), file=f)  # Export to QASM format
