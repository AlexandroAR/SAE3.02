import networkx as nx
import matplotlib.pyplot as plt

G=nx.read_adjlist("graphe1.txt", create_using=nx.DiGraph())

def AffichageGraphe(graphe):
    pos = nx.planar_layout(graphe)

    nx.draw_networkx_nodes(graphe, pos)
    nx.draw_networkx_edges(graphe, pos)
    nx.draw_networkx_labels(graphe, pos)


    print(f"Ce graphe contient {graphe.number_of_nodes()} sommets et {graphe.number_of_edges()} arêtes.")
    plt.show()

def arcs_arrivant(graphe):
    liste_arrivant = []

    for s in graphe.edges:
        if s[1] == "2":
            liste_arrivant.append(s)
    return liste_arrivant

def arcs_arrivantV2(graphe):
    liste_arrivant = []

    for s in graphe.predecessors("2"):
        arc = (s, "2")
        liste_arrivant.append(arc)
    return liste_arrivant

print(list(G.successors("2")))
print(arcs_arrivantV2(G))
AffichageGraphe(G)
