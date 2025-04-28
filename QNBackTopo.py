from QNBackClasses import *
from QNValidator import *


# Builds Topology of the Quantum Network
class topology:

    def __init__(self):
        # Initialize attributes to store connections and node tracking
        self.all_connections = []
        self.origin_to_destination_dict = {}
        self.visited_origin_nodes = set() 
        self.visited_destination_nodes = set()

    # Splits file to pull required information
    def parse_file(self, file_name):
        nodes = []
        qubits = None
        distance = []
        mode=''
        ideal_fidelity=0

        with open(file_name, 'r') as file:
            section = None 
            for line in file:
                line = line.strip() 

                if line == "-NODE-":
                    section = "NODE"
                    continue
                elif line == "-QUBITS-":
                    section = "QUBITS"
                    continue
                elif line == "-DISTANCE-":
                    section = "DISTANCE"
                    continue
                elif line == "-MODE-":
                    section = "MODE"
                    continue
                elif line == "-IDEAL FIDELITY-":
                    section = "IDEAL FIDELITY"
                    continue

                if section == "NODE":
                    if line: 
                        nodes.append(int(line))
                elif section == "QUBITS":
                    if line: 
                        qubits = int(line)
                elif section == "DISTANCE":
                    if line:
                        distance.append(float(line))
                elif section == "MODE":
                    if line:
                        mode = str(line)
                elif section == "IDEAL FIDELITY":
                    if line:
                        ideal_fidelity = float(line)

        return nodes, qubits, distance, mode, ideal_fidelity

class builder:
    # Builds the network based on the input file parsed above.
    def assemble_network(self, input_file):
        topo = topology()
        nodes, qubits, distance, mode, ideal_fidelity = topo.parse_file(input_file)
        qubit_idx = list(range(qubits))
        global_circuit = QuantumCircuit(qubits, qubits)

        validator = node_validator(nodes)
        verdict = validator.validate()
        gen = qubit_generator(qubits)
        qnode = quantum_node()
        fidelity_values=[]
        if verdict == True:
            mapList = []
            for i in nodes:
                if i  == 0:
                    origin = gen.generate_qubits()
                    global_circuit.compose(origin)
                    global_circuit.barrier()
                    mapList.append('origin')
                    continue
                elif i != 0 and i != 1:
                    coh_eval = coherence_evaluator(noise_level=0.01)
                    fidelity = coh_eval.evaluate_coherence(circuit=global_circuit, num_qubits=qubits, distance=distance)
                    fidelity_values.append(fidelity)
                    node = qnode.quantum_node_operation(circuit=global_circuit, fidelity=fidelity,ideal_fidelity=ideal_fidelity, qubit_idx = qubit_idx, mode=mode)
                    global_circuit.compose(node)
                    global_circuit.barrier()
                    mapList.append('node')
                    continue
                elif i == 1:
                    global_circuit.barrier()
                    mapList.append('destination')
                    continue
                else:
                    print("Error Composing Circuit: Possible Incorrect Node Input")
                    
        # THIS IS A WIRE LIST. I WAS THINKING IT COULD BE USED TO HELP BUILD THE COOLER GRAPH BUT DO WHATEVER IS EASIEST.
        wireList=()
        for i in range(len(mapList)):
            if i < len(mapList)-1 :
                wire_build = wire_maker(origin_node=mapList[i], destination_node=mapList[i+1], qubits=qubits, distance=distance[i])
                wire = wire_build.create_wire()
                wireList = wireList + (wire, )
            else:
                break
        # Applies Shors code to error check our network before measurement.
        shors_circuit = shors_QEC.shors_subcircuit(qubits)
        global_circuit.compose(shors_circuit, inplace=True)
    
        # Measures to get the output of the circuit.
        global_circuit.measure_all()

        # Returns the Circuit and Fidelity values from the Coherence checks between each node.
        return global_circuit, fidelity_values
