import networkx as nx
import matplotlib.pyplot as plt
import ap

def ExtractionDesAP(fichier):
    aps = []
    with open(fichier, 'r') as f:
        lignes = f.readlines()
    for x in lignes:
        x.strip()
        index = int(x[:2])
        rayon = int(x[-3:])
        coord = x[x.find('(')+1:x.find(')')]
        coord = coord.split(",")
        coord = (int(coord[0]), int(coord[1]))
        a = ap.AP(index, coord, rayon)
        aps.append(a)
    return aps

def topologie():
    topo = nx.Graph()
    for x in ExtractionDesAP("Test/test_AP.txt"):
        topo.add_node(x.index, coord=x.coord)
    return topo

def affichage(graphe):
    pos = nx.get_node_attributes(graphe,'coord')
    nx.draw_networkx_nodes(graphe, pos)
    nx.draw_networkx_labels(graphe, pos)
    plt.show()

affichage(topologie())


