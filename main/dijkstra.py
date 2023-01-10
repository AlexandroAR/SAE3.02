import networkx as nx
import matplotlib.pyplot as plt
import math

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
