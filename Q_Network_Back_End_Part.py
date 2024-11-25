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
    def __init__(self, num_qubits=4, state='zero'):
        self.num_qubits = num_qubits
        self.state = state

    def generate_qubits(self):
        circuit = QuantumCircuit(self.num_qubits)
        if self.state == 'plus':
            circuit.h(range(self.num_qubits))  # Hadamard to create |+⟩ state
        elif self.state == 'entangled' and self.num_qubits > 1:
            circuit.h(0)
            for i in range(1, self.num_qubits):
                circuit.cx(0, i)  # Create Bell pairs
        # Other states could be added similarly
        return circuit

class quantum_node:
    def __init__(self, id): # Constructor
        # Initialize attributes here
        self.id = parameters[0]
        # and so on

    # See section on Quantum Nodes
    def quantum_node_operation(self, circuit, qubit_idx=0, mode='random', num_operations=3):

 #   Apply a quantum node operation on a given qubit in the circuit.

#    Parameters:
#    - circuit: QuantumCircuit - The circuit on which to operate.
#    - qubit_idx: int - Index of the qubit to operate on.
#    - mode: str - 'random' for random operations or 'rigorous' for a specific sequence.
#    - num_operations: int - Number of operations for random mode.

#    Returns:
#    - QuantumCircuit with applied operations.
 
        if mode == 'random':
            # Apply a sequence of random operations
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
                    # For CX gate, ensure there's a second qubit to act as the target
                    target_qubit = (qubit_idx + 1) % circuit.num_qubits
                    circuit.cx(qubit_idx, target_qubit)

        elif mode == 'rigorous':
            # Apply a predefined rigorous sequence of transformations
            circuit.h(qubit_idx)
            circuit.t(qubit_idx)
            circuit.x(qubit_idx)
            circuit.s(qubit_idx)
            circuit.z(qubit_idx)
            circuit.y(qubit_idx)
            circuit.cx(qubit_idx, (qubit_idx + 1) % circuit.num_qubits)  # CNOT with the next qubit (if available)

        return circuit

class wire:
  def __init__(self, origin_node, destination_node, size, distance): # Constructor
    # Node of origin for qubit transfers
    self.origin_node = origin_node
    # Node in which is the destination for qubit transfers
    self.destination_node = destination_node
    # Number of qubits in which can be transfered at once over this wire
    self.size = size
    # Distance between nodes in meters
    self.distance = distance

  def set_origin_node(self, new_origin):
    self.origin_node = new_origin

  def set_destination_node(self, new_destination): # Class method
    self.destination_node = new_destination

  def set_size(self, new_size): # Class method
    self.size = new_size

  def set_distance(self, new_distance): # Class method
    self.distance = new_distance

  # TODO: Finish this
  def transport_qubit(self, circuit, qubit_idx):
    # Example coherence-preserving operation during "transport"
    circuit.i(qubit_idx)  # Identity gate as placeholder
    return circuit

class qubit_transporter:
    def __init__(self, circuit):
        self.circuit = circuit

    def transport_qubit(self, qubit_idx):
        # Example coherence-preserving operation during "transport"
        self.circuit.i(qubit_idx)  # Identity gate as placeholder
        return self.circuit
    
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
        backend = Aer.get_backend('statevector_simulator')
        noisy_result = execute(circuit, backend, noise_model=noise_model).result()
        noisy_state = noisy_result.get_statevector()

        # Step 4: Calculate fidelity between ideal and noisy state
        fidelity = state_fidelity(ideal_state, noisy_state)

        return fidelity
    
class qubit_measurer:
    def __init__(self, circuit):
        self.circuit = circuit

    def measure_qubits(self):
        # Measure all qubits in the circuit
        num_qubits = self.circuit.num_qubits
        self.circuit.measure_all()
        return self.circuit

class shors_QEC:
    def __init__(self):
        # Initialize the quantum and classical registers
        self.data_qubits = QuantumRegister(9, 'data')  # 9 qubits for Shor's code
        self.ancilla_bits = ClassicalRegister(1, 'ancilla')  # For measurement results
        self.circuit = QuantumCircuit(self.data_qubits, self.ancilla_bits)

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

