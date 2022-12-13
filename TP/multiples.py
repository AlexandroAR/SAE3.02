import networkx as nx
import matplotlib.pyplot as plt

G=nx.DiGraph()

for k in range(1,13):
    for p in range(1, 13):
        if (p%k == 0):
            G.add_edge(k, p)

def AffichageGraphe(graphe):
    pos = nx.circular_layout(graphe)

    nx.draw_networkx_nodes(graphe, pos, node_size=500)
    nx.draw_networkx_edges(graphe, pos, arrowsize=20)
    nx.draw_networkx_labels(graphe, pos)

    print(f"Ce graphe contient {graphe.number_of_nodes()} sommets et {graphe.number_of_edges()} arêtes.")
    plt.show()

G.remove_edge(7, 7)
print(G.nodes(), G.edges())
AffichageGraphe(G)