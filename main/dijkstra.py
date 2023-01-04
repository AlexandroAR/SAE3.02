import networkx as nx
import matplotlib.pyplot as plt
import math

def dijkstra(graphe, E):
    distances = {E: 0}
    for noeud in graphe.nodes:
        if noeud != E:
            distances[noeud] = 0
    traites = []
    poids = nx.get_edge_attributes(graphe, 'poids')
    S = E

    queue = ''
    while S not in traites:
        min = math.inf
        for voisin in graphe.neighbors(S):
            if S < voisin:
                sv = (S, voisin)
            elif S > voisin:
                sv = (voisin, S)

            if poids[sv] < min and voisin not in traites:
                min = poids[sv]
                queue = voisin
            if voisin != E:
                distances[voisin] = distances[S] + poids[sv]
        traites.append(S)
        print(traites)
        S = queue
        print(S)
        print(distances)

    return distances

G = nx.gnm_random_graph(n=10, m=20)
for u, v in G.edges():
    nx.set_edge_attributes(G, 1, 'poids')

dijkstra(G, 1)
nx.draw(G, with_labels=True)
plt.show()
