from QNBackClasses import *
from QNValidator import *



class topology:

    def __init__(self):
        # Initialize attributes to store connections and node tracking
        self.all_connections = []
        self.origin_to_destination_dict = {}
        self.visited_origin_nodes = set() 
        self.visited_destination_nodes = set()

    def parse_file(self, file_name):
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

class builder:

    def assemble_network(self, input_file, ideal_fidelity:float):
        topo = topology()
        nodes, qubits, distance = topo.parse_file(input_file)
        qubit_idx = list(range(qubits))
        global_circuit = QuantumCircuit(qubits, qubits)

        validator = node_validator(nodes)
        verdict = validator.validate()
        gen = qubit_generator(qubits)
        qnode = quantum_node()
        if verdict == True:
            mapList = []
            for i in nodes:
                if nodes[i]  == 0:
                    origin = gen.generate_qubits()
                    global_circuit.compose(origin, inplace=True)
                    global_circuit.barrier()
                    mapList.append('origin')
                elif nodes[i] != 1 or nodes[i] != 0:
                    coh_eval = coherence_evaluator()
                    fidelity = coh_eval.evaluate_coherence(global_circuit, qubits)
                    node = qnode.quantum_node_operation(circuit=global_circuit, fidelity=fidelity,ideal_fidelity=ideal_fidelity, qubit_idx = qubit_idx, mode='rigorous')
                    global_circuit.compose(node, inplace=True)
                    global_circuit.barrier()
                    mapList.append('node')
                elif nodes[i] == 1:
                    global_circuit.barrier()
                    mapList.append('destination')
                    break
        
        wireList=()
        for i in range(len(mapList)):
            if i < len(mapList)-1 :
                wire_build = wire_maker(origin_node=mapList[i], destination_node=mapList[i+1], size=qubits, distance=distance)
                wire = wire_build.create_wire()
                wireList = wireList + (wire, )
            else:
                break
        shors_circuit = shors_QEC.shors_subcircuit(qubits)
        global_circuit.compose(shors_circuit, inplace=True)
    

        global_circuit.measure(range(qubits), range(qubits))

        return global_circuit
