import networkx as nx
import matplotlib.pyplot as plt

G=nx.graph_atlas(666)

def AffichageGraphe(graphe):
    pos = nx.circular_layout(graphe)

    nx.draw_networkx_nodes(graphe, pos, node_size=500)
    nx.draw_networkx_edges(graphe, pos, arrowsize=20)
    nx.draw_networkx_labels(graphe, pos)

    print(f"Ce graphe contient {graphe.number_of_nodes()} sommets et {graphe.number_of_edges()} arêtes.")
    plt.show()

def liste_degrés(graphe):
    degrés = []
    for deg in nx.degree(graphe):
        degrés.append(deg[1])
    return degrés


print(liste_degrés(G))
AffichageGraphe(G)
nx.write_adjlist(G, "Atlas.txt")


