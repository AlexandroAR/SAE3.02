import networkx as nx
import matplotlib.pyplot as plt

G=nx.Graph()

G.add_edges_from([("Routeur 1", "Routeur 2"),
                  ("Routeur 1", "Routeur 3"),
                  ("Routeur 1", "Routeur 4"),
                  ("Routeur 2", "Routeur 4"),
                  ("Routeur 2", "Routeur 5"),
                  ("Routeur 3", "Routeur 4"),
                  ("Routeur 4", "Routeur 5")])

def AffichageGraphe(graphe):
    pos = nx.planar_layout(graphe)

    nx.draw_networkx_nodes(graphe, pos, node_size=4000)
    nx.draw_networkx_edges(graphe, pos)
    nx.draw_networkx_labels(graphe, pos)
    nx.draw_networkx_edge_labels(G, pos, )

    print(f"Ce graphe contient {graphe.number_of_nodes()} sommets et {graphe.number_of_edges()} arêtes.")
    plt.show()

G.add_edge("Routeur 1","Routeur 3",liaison="FastEthernet",support='cuivre')
print(G["Routeur 3"]["Routeur 1"])
AffichageGraphe(G)