import networkx as nx
import matplotlib.pyplot as plt
import ap

def ExtractionDesAP(fichier_ap, fichier_apc):
    aps = []
    apcs = []
    with open(fichier_ap, 'r') as f:
        lignes = f.readlines()

    with open(fichier_apc, 'r') as f:
        apcs = f.readline().strip().split(' ')

    for x in lignes:
        x.strip()
        index = x[:2].strip()
        rayon = x[-3:].strip()

        coord = x[x.find('(')+1:x.find(')')]
        coord = coord.split(",")
        coord = (int(coord[0]), int(coord[1]))

        if index in apcs:
            couleur = 'blue'
            type_ap = 'C'
        else:
            couleur = 'red'
            type_ap = 'S'

        a = ap.AP(int(index), coord, int(rayon), couleur, type_ap)
        aps.append(a)
        print(a)
    return aps

def topologie():
    topo = nx.Graph()
    for x in ExtractionDesAP("Test/test_AP.txt", "Test/test_APC.txt"):
        topo.add_node(x.index, coord=x.coord, couleur=x.color)
    return topo

def affichage(graphe):
    colors = []
    pos = nx.get_node_attributes(graphe,'coord')
    col = nx.get_node_attributes(graphe, 'couleur')
    for x in col:
        colors.append(col[x])
    nx.draw_networkx_nodes(graphe, pos, node_color=colors)
    nx.draw_networkx_labels(graphe, pos)
    plt.show()

affichage(topologie())


