from QNBackTopo import *
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister, transpile
 
builder = builder()
bob_circuit = builder.assemble_network('/Users/j03/Desktop/Coding/GitHub/Q-Network-Simulator/QN-dummy.txt', 0.5)
# Create Universal simulator - DONE
# Create and build a network
# Produce visual of network
# Retrieve output of network
# Esnure that output is as desired


simulator = AerSimulator.get_backend('qasm_simulator')
result = transpile(bob_circuit, simulator, shots=1024).result()
counts = result.get_counts()

