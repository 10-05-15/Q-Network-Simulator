from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Kraus, SuperOp
from qiskit.visualization import plot_histogram
from qiskit_aer.noise import (NoiseModel, QuantumError, ReadoutError,
    pauli_error, depolarizing_error, thermal_relaxation_error)

from qiskit.quantum_info import Statevector, state_fidelity
import numpy as np



class qubit_generator:
    def __init__(self, num_qubits, state):
        self.num_qubits = num_qubits
        self.state = state

    def generate_qubits(self):

        circuit = QuantumCircuit(self.num_qubits)

        if self.qubits == 1:
            self.state == 'plus'
        elif self.qubits > 1:
            self.state == 'entangled'

        if self.state == 'plus':
            circuit.h(range(self.num_qubits)) 
        elif self.state == 'entangled' and self.num_qubits > 1:
            circuit.h(0)
            for i in range(1, self.num_qubits):
                circuit.cx(0, i) 
        return circuit

class quantum_node:

    def quantum_node_operation_random(self, circuit, fidelity, ideal_fidelity, qubit_idx, mode='random', num_operations=3):
        if fidelity >= ideal_fidelity:
            for _ in range(num_operations):
                gate_choice = np.random.choice(['h', 'x', 'y', 'z', 's', 't', 'cx'])
                if gate_choice == 'h':
                    circuit.h(qubit_idx)
                elif gate_choice == 'x':
                    circuit.x(qubit_idx)
                elif gate_choice == 'y':
                    circuit.y(qubit_idx)
                elif gate_choice == 'z':
                    circuit.z(qubit_idx)
                elif gate_choice == 's':
                    circuit.s(qubit_idx)
                elif gate_choice == 't':
                    circuit.t(qubit_idx)
                elif gate_choice == 'cx':
                    target_qubit = (qubit_idx + 1) % circuit.num_qubits
                    circuit.cx(qubit_idx, target_qubit)
                else: 
                    break
            return circuit
        else: 
            print ("Error: Qubits did not maintain coherence")


    def quantum_node_operation_rigorous(self, circuit, fidelity, ideal_fidelity, qubit_idx, mode='rigourous'):
        if fidelity >= ideal_fidelity:
            circuit.h(qubit_idx)
            circuit.t(qubit_idx)
            circuit.x(qubit_idx)
            circuit.s(qubit_idx)
            circuit.z(qubit_idx)
            circuit.y(qubit_idx)
            circuit.cx(qubit_idx, (qubit_idx + 1) % circuit.num_qubits) 
            return circuit
        else: 
            print ("Error: Qubits did not maintain coherence")

    def quantum_node_operation_series(self, circuit, fidelity, ideal_fidelity, qubit_idx, mode='series', series_vector=['h', 't', 'x', 's', 'z', 'y', 'cx']):
        if fidelity >= ideal_fidelity:
            for gate_type in series_vector:
                if gate_type == 'h':
                    circuit.h(qubit_idx)
                elif gate_type == 'x':
                    circuit.x(qubit_idx)
                elif gate_type == 'y':
                    circuit.y(qubit_idx)
                elif gate_type == 'z':
                    circuit.z(qubit_idx)
                elif gate_type == 's':
                    circuit.s(qubit_idx)
                elif gate_type == 't':
                    circuit.t(qubit_idx)
                elif gate_type == 'cx':
                    target_qubit = (qubit_idx + 1) % circuit.num_qubits
                else:
                    break
            return circuit
        else: 
            print ("Error: Qubits did not maintain coherence")
    

class wire:
  def __init__(self, origin_node, destination_node, size, distance):
    self.origin_node = origin_node
    self.destination_node = destination_node
    self.size = size
    self.distance = distance

  def set_origin_node(self, new_origin):
    self.origin_node = new_origin

  def set_destination_node(self, new_destination):
    self.destination_node = new_destination

  def set_size(self, new_size):
    self.size = new_size

  def set_distance(self, new_distance):
    self.distance = new_distance

  # TODO: Finish this
  def transport_qubit(self, circuit, qubit_idx):
    circuit.i(qubit_idx)
    return circuit

class qubit_transporter:
    def __init__(self, circuit):
        self.circuit = circuit

    def transport_qubit(self, qubit_idx):
        # Example coherence-preserving operation during "transport"
        self.circuit.i(qubit_idx)  # Identity gate as placeholder
        return self.circuit
    
'''   
class qubit_measurer:
    def __init__(self, circuit):
        self.circuit = circuit

    def measure_qubits(self):
        end = []
        # Measure all qubits in the circuit
        num_qubits = self.circuit.num_qubits
        self.circuit.measure_all()

        end.append(self.circuit)
        return end
'''
    
class coherence_evaluator:
    def __init__(self, noise_level=0.01):
        # Initialize with a default noise level, which can be modified
        self.noise_level = noise_level

    def evaluate_coherence(self, circuit):
        # Step 1: Generate the ideal state vector from the input circuit
        ideal_state = Statevector.from_instruction(circuit)

        # Step 2: Define the noise model to simulate decoherence
        noise_model = NoiseModel()
        # Apply depolarizing noise to all qubits in the circuit
        error = depolarizing_error(self.noise_level, 1)
        noise_model.add_all_qubit_quantum_error(error, ['id', 'h', 'cx'])

        # Step 3: Run the input circuit with noise
        backend = AerSimulator.get_backend('statevector_simulator')
        noisy_result = transpile(circuit, backend, noise_model=noise_model).result()
        noisy_state = noisy_result.get_statevector()

        # Step 4: Calculate fidelity between ideal and noisy state
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
    
    def shors_code_qec(self):
        # Step 1: Encode a logical qubit using Shor's code
        # Initialize the first qubit to |+⟩
        self.circuit.h(self.data_qubits[0])
        for i in [1, 2]:
            self.circuit.cx(self.data_qubits[0], self.data_qubits[i])  # Create GHZ state (|000⟩ + |111⟩) / sqrt(2)

        # Repeat this for the remaining pairs of three qubits to fully encode
        for i in range(0, 9, 3):
            self.circuit.cx(self.data_qubits[i], self.data_qubits[i + 1])
            self.circuit.cx(self.data_qubits[i], self.data_qubits[i + 2])

        # Step 2: Syndrome Measurement for error detection
        # Measure parity checks to detect bit-flip errors
        for i in range(3):
            self.circuit.cx(self.data_qubits[3 * i], self.data_qubits[3 * i + 1])
            self.circuit.cx(self.data_qubits[3 * i], self.data_qubits[3 * i + 2])

        # Step 3: Decode back to single qubit (simplified version)
        for i in range(1, 9):
            self.circuit.cx(self.data_qubits[0], self.data_qubits[i])  # Undo encoding to retrieve logical qubit

        # Step 4: Measure to confirm correction
        self.circuit.measure(self.data_qubits[0], self.ancilla_bits[0])

        return self.circuit
    


