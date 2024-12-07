from QNBackClasses import *
from QNValidator import *



class topology:

    def __init__(self):
        # Initialize attributes to store connections and node tracking
        self.all_connections = []
        self.origin_to_destination_dict = {}
        self.visited_origin_nodes = set() 
        self.visited_destination_nodes = set()

    def parse_file(file_name):
        nodes = []
        qubits = None
        distance = None

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

                if section == "NODE":
                    if line: 
                        nodes.append(int(line))
                elif section == "QUBITS":
                    if line: 
                        qubits = int(line)
                elif section == "DISTANCE":
                    if line:
                        distance = float(line)
        return nodes, qubits, distance 

    def create_topology(self, nodes, qubits, distance):
        validator = node_validator(nodes)
        verdict = validator.validate()
        if verdict == True:
            mapList = []
            for i in nodes:
                if nodes[i]  == 0:
                    origin = qubit_generator.generate_qubits(qubits)
                    mapList.append(origin)
                elif nodes[i] != 1 and nodes[i] != 0:
                    node = quantum_node.quantum_node_operation()
                    mapList.append(node)
                elif nodes[i] == 1:
                    break

            wireList=[]
            for i in mapList:
                wire = wire.wire(mapList[i], mapList[i+1], wire_size=qubits, node_distance=distance)
                wireList.apped(wire)
            return mapList, wireList

class builder:

    def assemble_network(self, input_file, ideal_fidelity:float):
        topo = topology()
        nodes, qubits, distance = topo.parse_file(input_file)
        wires, mapping = topo.create_topology(nodes, qubits, distance)

        global_circuit = QuantumCircuit(qubits, qubits)
        for idx, node in enumerate(mapping):
            if isinstance(node, qubit_generator):
                generated = node.generate_qubits()
                global_circuit.compose(generated[0], inplace=True)
            elif isinstance(node, quantum_node):
                qubit_idx = idx % qubits
                fidelity=coherence_evaluator.evaluate_coherence(global_circuit)
                circuit = node.quantum_node_operation(global_circuit, fidelity, ideal_fidelity, qubit_idx)
                global_circuit.compose(circuit, inplace=True)
        
        for wire in wires:
            for qubit_idx in range(wire.size):
                wire.transport_qubit(global_circuit, qubit_idx)
        
        shors_circuit = shors_QEC.shors_subcircuit(qubits)
        global_circuit.compose(shors_circuit, inplace=True)
    

        global_circuit.measure(range(qubits), range(qubits))

        return global_circuit






        

    # Going to establish the wires and map into a fixed form here maybe cast to a 2D array?
    # Need to add coherence evaluator are every point and ensure that before it goes to the
    # last node it hits the shors_QEC method. Also, may need to rework final node. Cannot 
    # let it exist as a node since it just calls measure all automatically and will collpase 
    # the state.



