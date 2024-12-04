from Q_Network_Back_End_Parts import *
from Q_Network_Connection_Logic import *

qubit_generator=qubit_generator()
quantum_node=quantum_node()
wire=wire()
qubit_transporter=qubit_transporter()
coherence_evaluator=coherence_evaluator()
qubit_measurer=qubit_measurer()
shors_qec=shors_QEC()
node_validator=node_validator()

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
        verdict = node_validator.validate (nodes)
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

    def assemble_network(self, input_file, ideal_fidelity):
        nodes, qubits, distance = topology.parse_file(input_file)
        wires, mapping = topology.create_topology(nodes, qubits, distance)
        simulator = AerSimulator()

        global_circuit = QuantumCircuit()
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
        
        
        global_circuit.measure_all()

        transpiled_circuit = transpile(global_circuit, simulator)
        result = simulator.run(transpiled_circuit).result()
        counts = result.get(counts)

        print("Simulation Complete. Results:")
        print(counts)
        return global_circuit, counts





        

    # Going to establish the wires and map into a fixed form here maybe cast to a 2D array?
    # Need to add coherence evaluator are every point and ensure that before it goes to the
    # last node it hits the shors_QEC method. Also, may need to rework final node. Cannot 
    # let it exist as a node since it just calls measure all automatically and will collpase 
    # the state.



