from QNBackTopo import *
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister, transpile
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


builder = builder()
# BE SURE TO CHANGE FILE PATH ON USERS PC
bob_circuit, fidelity_values = builder.assemble_network('/Users/j03/Desktop/Coding/GitHub/Q-Network-Simulator/QN-dummy.txt')

# Distance Degredation effect - DONE
# Cooler looking network map - WORK IN PROGRESS



backend = AerSimulator(method='automatic')
qnet_circuit = transpile(bob_circuit, backend, num_processes=1024)
job = backend.run(qnet_circuit)
result = job.result()
counts = result.get_counts()

print(fidelity_values)

# Current plots we have, please keep them around even after the new plots are made.
histogram = plot_histogram(counts)
circuit_plot = bob_circuit.draw(output='mpl')

plt.show()
