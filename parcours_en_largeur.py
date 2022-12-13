import math
import time
import scipy as sp

import networkx as nx
import matplotlib.pyplot as plt



G=nx.read_adjlist("graphe1.txt", create_using=nx.Graph())

G1 = nx.Graph()
G1.add_node("A")

#G2 = nx.random_regular_graph(500, 1000)

def Initialisation(graphe, E):
    nx.set_node_attributes(graphe, "blanc", "Couleur")
    nx.set_node_attributes(graphe, math.inf, "Distance")

    graphe.nodes[E]["Couleur"] = "vert"
    graphe.nodes[E]["Distance"] = 0

    sommets_traitement = [E]
    Arbre = nx.Graph()

    return sommets_traitement, Arbre

def Traitement(graphe, liste, arbre):
    if graphe.number_of_nodes() == 1:
        arbre.add_node(liste[0])
    while len(liste) > 0:
        S = liste[0]
        for V in graphe.neighbors(S):
            if graphe.nodes[V]["Couleur"] == "blanc":
                graphe.nodes[V]["Distance"] = graphe.nodes[S]["Distance"] + 1
                liste.append(V)
                graphe.nodes[V]["Couleur"] = "vert"
                arbre.add_edge(S, V)
        graphe.nodes[S]["Couleur"] = "rouge"
        liste.remove(S)

    return arbre

def parcours_en_largeur(graphe, E):
    liste, arbre = Initialisation(graphe, E)
    return Traitement(graphe, liste, arbre)

def AffichageGraphe(graphe):
    pos = nx.planar_layout(graphe)
    nx.draw_networkx_nodes(graphe, pos)
    nx.draw_networkx_edges(graphe, pos)
    nx.draw_networkx_labels(graphe, pos)


def est_connexe(G, E):
    H = parcours_en_largeur(G, E)
    if G.number_of_nodes() == H.number_of_nodes():
        return True
    else:
        return False

def composantes_connexes(G):
    alph = []
    for x in G.nodes:
        alph.append(x)
    print(alph)
    composantes = []
    while len(alph) > 1:
        composante = parcours_en_largeur(G, alph[0])
        composantes.append(composante)
        alph = set(composante.nodes).symmetric_difference(set(alph))
        alph = list(alph)
        print(alph)


    return composantes

for composante in composantes_connexes(G):
    print(composante)
    AffichageGraphe(composante)

#AffichageGraphe(G)
plt.show()
