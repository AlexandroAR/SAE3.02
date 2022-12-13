import networkx as nx
import matplotlib.pyplot as plt

G=nx.barbell_graph(4,0)

def AffichageGraphe(graphe):
    pos = nx.circular_layout(graphe)

    nx.draw_networkx_nodes(graphe, pos)
    nx.draw_networkx_edges(graphe, pos)
    nx.draw_networkx_labels(graphe, pos)

    print(f"Ce graphe contient {graphe.number_of_nodes()} sommets et {graphe.number_of_edges()} arêtes.")
    plt.show()

AffichageGraphe(G)