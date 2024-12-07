'''
PLEASE NOTE THAT I CHANGED THE FORMAT OF HOW THE INPUT FILES SHOULD BE RECIEVED TO READ
AS FOLLOWS:

*******************************************

-NODE-
Origin
Node1
Node2
. . .
NodeN
End
-QUBITS-
XXX
-DISTANCE-
XXX

*******************************************

With the following rules being installed and verified below:
Origin can connect to any node.
Any node can connect to any other node PROVIDED it is the only node connected to that node.
Last node receives one input PER simulation and can not give a value to any other node.
Nodes can (AS OF NOW) only recieve one input and give one output.
'''

class node_validator:
    def __init__(self, nodes_list):
        self.nodes_list = nodes_list
        self.origin_connected = False
        self.final_connected = False
        self.intermediate_connections = {}

    def validate(self):
        print(self.nodes_list)
        for i, node in enumerate(self.nodes_list):
            if node == 0:  
                if self.origin_connected:  
                    print("Error: Origin node (Node 0) already has a connection.")
                    return False
                self.origin_connected = True

            elif node == 1:  
                if self.final_connected:
                    print("Error: Final node (Node 1) already has an outgoing connection.")
                    return False
                self.final_connected = True
            else:
                if node in self.intermediate_connections:
                    print(f"Error: Node {node} is already connected.")
                    return False
                self.intermediate_connections[node] = {"in": False, "out": False}

        for i, node in enumerate(self.nodes_list):
            if node == 0: 
                continue
            if node == 1: 
                continue

            # ADD MORE CHECKS HERE LATER IF NEEDED 

        return True
