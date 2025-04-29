from QNBackTopo import *
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit import ClassicalRegister, QuantumRegister, transpile
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram
from pyflowchart import Flowchart, Node
from graphviz import Digraph


builder = builder()
# BE SURE TO CHANGE FILE PATH ON USERS PC
bob_circuit, fidelity_values, nodes, distances, qubits, mode, ideal_fidelity = builder.assemble_network('/Users/j03/Desktop/Coding/GitHub/Q-Network-Simulator/QN-dummy.txt')

# Distance Degredation effect - DONE
# Cooler looking network map - DONE

dot = Digraph('QuantumNetwork', format='png')

        # Define nodes
for node in nodes:
    dot.node(str(node), f'Node {node}')

        # Define edges with distances
for i in range(len(nodes) - 1):
    start = str(nodes[i])
    end = str(nodes[i + 1])
    distance = distances[i]
    dot.edge(start, end, label=f'{distance} km')

        # Add a "legend" as a separate cluster
with dot.subgraph(name='cluster_legend') as c:
    c.attr(label='Legend')
    c.node('Q', f'Qubits: {qubits}')
    c.node('M', f'Mode: {mode}')
    c.node('F', f'Ideal Fidelity: {ideal_fidelity}')
    c.attr(style='dashed')

dot.render('QuantumNetwork', view=True)


#bob_chart.render('quantum_network_graph', view=True)
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
