from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Kraus, SuperOp
from qiskit.visualization import plot_histogram
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)

from qiskit.quantum_info import Statevector, state_fidelity
import numpy as np

class qubit_generator:
    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
    
    def generate_qubits(self):
        circuit = QuantumCircuit(self.num_qubits)
        state=''
        if self.num_qubits == 1:
            state == 'plus'
        elif self.num_qubits > 1:
            state == 'entangled'

        if state == 'plus':
            circuit.h(range(self.num_qubits))  
        elif state == 'entangled' and self.num_qubits > 1:
            circuit.h(0)
            for i in range(1, self.num_qubits):
                circuit.cx(0, i) 
        return circuit

class quantum_node:

    def __init__(self):
        self.gate_map = {
            'h': lambda circuit, i: circuit.h(i),
            'x': lambda circuit, i: circuit.x(i),
            'y': lambda circuit, i: circuit.y(i),
            'z': lambda circuit, i: circuit.z(i),
            's': lambda circuit, i: circuit.s(i),
            't': lambda circuit, i: circuit.t(i),
            'cx': lambda circuit, i: circuit.cx(i, (i + 1) % circuit.num_qubits)
        }

    def apply_gates(self, circuit, qubit_idx, gates):
        for gate in gates:
            for i in qubit_idx:
                self.gate_map[gate](circuit, i)
        return circuit
   
    def quantum_node_operation(self, circuit, fidelity, ideal_fidelity, qubit_idx, mode: str, num_operations=1, series_vector=['h', 't', 'x', 's', 'z', 'y', 'cx']):
        if fidelity < ideal_fidelity:
            print("Error: Qubits did not maintain coherence")
            return circuit

        if mode == 'random':
            gates = [np.random.choice(list(self.gate_map.keys())) for _ in range(num_operations)]
        elif mode == 'rigorous':
            gates = ['h', 't', 'x', 's', 'z', 'y', 'cx']
        elif mode == 'series' and series_vector:
            gates = series_vector
        else:
            print("Error: Invalid mode or missing series_vector")
            return circuit

        return self.apply_gates(circuit, qubit_idx, gates)


class wire_maker:
  def __init__(self, origin_node, destination_node, size, distance):
    self.origin_node = origin_node
    self.destination_node = destination_node
    self.size = size
    self.distance = distance

  def create_wire(self):
      wire=[]
      wire.append(self.origin_node)
      wire.append(self.destination_node)
      wire.append(self.size)
      wire.append(self.distance)
      return wire

  # TODO: FINISH COHERENCE BEFORE ADDRESSING
  def transport_qubit(self, circuit, qubit_idx):
    circuit.i(qubit_idx)
    return circuit
    
class coherence_evaluator:
    def __init__(self, noise_level=0.01):
        # Initialize with a default noise level, which can be modified
        self.noise_level = noise_level

    def evaluate_coherence(self, circuit, num_qubits):
        # Step 1: Generate the ideal state vector from the input circuit
        ideal_state = Statevector.from_instruction(circuit)

        # Step 2: Define the noise model to simulate decoherence
        noise_model = NoiseModel()
        # NEED TO MAKE MORE RIGOROUS IN FUTURE ITERATIONS
        error = depolarizing_error(self.noise_level, num_qubits)
        noise_model.add_all_qubit_quantum_error(error, ['cx'])

        backend = AerSimulator(method='statevector', noise_model=noise_model)
        noisy_circuit = transpile(circuit, backend)
        noisy_circuit.save_statevector()
        job = backend.run(noisy_circuit)
        noisy_result = job.result()
        noisy_result.get_statevector(noisy_circuit, decimals=10)
        noisy_state = noisy_result.get_statevector()
        fidelity = state_fidelity(ideal_state, noisy_state)

        return fidelity
    

class shors_QEC:
    def __init__(self):
        # Initialize the quantum and classical registers
        self.data_qubits = QuantumRegister(9, 'data')  # 9 qubits for Shor's code
        self.ancilla_bits = ClassicalRegister(1, 'ancilla')  # For measurement results
        self.circuit = QuantumCircuit(self.data_qubits, self.ancilla_bits)

    def shors_subcircuit(qubits):
        if qubits < 1 or qubits > 4:
            raise ValueError("")
        qc = QuantumCircuit(qubits)
        qc.h(range(qubits))
        qft_circuit = QFT(qubits).decompose()
        qc.append(qft_circuit, range(qubits))
        return qc
