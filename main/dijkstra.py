import networkx as nx
import matplotlib.pyplot as plt
import math

# def dijkstraDEMO(graphe, E):
#     distances = {noeud: math.inf for noeud in graphe.nodes}
#     distances[E] = 0
#     traites = []
#     poids = nx.get_edge_attributes(graphe, 'poids')
#     S = E

#     queue = ''
#     while S not in traites:
#         min = math.inf
#         for voisin in graphe.neighbors(S):
#             if S < voisin:
#                 sv = (S, voisin)
#             elif S > voisin:
#                 sv = (voisin, S)

#             if poids[sv] < min and voisin not in traites:
#                 min = poids[sv]
#                 queue = voisin
#             if voisin != E and ((distances[S] + poids[sv]) < distances[voisin]):
#                 distances[voisin] = distances[S] + poids[sv]
#         traites.append(S)
#         S = queue

#     return distances

def dijkstra(graphe, E):
    queue, distances, predeceseurs = [], {}, {}

    for noeud in graphe.nodes:
        queue.append(noeud)
        distances[noeud] = math.inf
        predeceseurs[noeud] = None

    distances[E] = 0
    min = math.inf

    while len(queue) > 0:
        for S in queue:
            if distances[S] < min:
                u = S
        if u in queue:
            queue.remove(u)
            for v in graphe.neighbors(u):
                if v in queue:
                    dist = distances[u] + graphe[u][v]['poids']
                    if dist < distances[v]:
                        distances[v] = dist
                        predeceseurs[v] = u
        else:
            break
    
    # print(distances)
    # print(predeceseurs)
    return distances

# G = nx.gnm_random_graph(n=10, m=20)
# for u, v in G.edges():
#     nx.set_edge_attributes(G, 1, 'poids')

# dijkstra2(G, 1)
# nx.draw(G, with_labels=True)
# plt.show()
