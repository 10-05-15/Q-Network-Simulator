from QNBackTopo import *
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister, transpile
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


builder = builder()
bob_circuit = builder.assemble_network('/Users/j03/Desktop/Coding/GitHub/Q-Network-Simulator/QN-dummy.txt', 0.5)
# Create Universal simulator - DONE
# Create and build a network - DONE
# Produce visual of network
# Retrieve output of network - DONE
# Esnure that output is as desired



backend = AerSimulator(method='automatic')
qnet_circuit = transpile(bob_circuit, backend, num_processes=1024)
job = backend.run(qnet_circuit)
result = job.result()
counts = result.get_counts()

histogram = plot_histogram(counts)
circuit_plot = bob_circuit.draw(output='mpl')

plt.show()
