import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import datetime
import ap
import dijkstra as dij
import math


def ExtractionDesAP(fichier_ap, fichier_apc):

    #Liste et dictionnaire des AP et AP controleurs
    aps = {}
    apcs = []

    #Extraction des lignes (APs) dans une liste
    with open(fichier_ap, 'r') as f:
        lignes = f.readlines()

    #Création de liste d'index des AP controleurs
    with open(fichier_apc, 'r') as f:
        apcs = f.readline().strip().split(' ')

    #Boucle de création des AP
    for x in lignes:
        x.strip()
        
        #Extraction de l'index (2 premiers caractères)
        index = x[:2].strip()

        #Extraction du rayon (2 derniers caractères)
        rayon = x[-4:].strip()

        #Extraction des coordonnées dans tuple coord
        coord = x[x.find('(')+1:x.find(')')]
        coord = coord.split(",")
        coord = (int(coord[0]), int(coord[1]))

        #Triage de mode et couleur de AP
        if index in apcs:
            couleur = 'blue'
            type_ap = 'C'
        else:
            couleur = 'gray'
            type_ap = 'S'

        #Création d'un objet AP et ajout en dictionnaire des AP
        a = ap.AP(index, coord, int(rayon), couleur, type_ap)
        aps[index] = a
        print(a)

    return aps

def topologie():

    #Création graphe représentant la topologie
    topo = nx.Graph()

    aps = ExtractionDesAP("Test/test_AP.txt", "Test/test_APC.txt")
    arrets = {}

    #Ajout des sommets représentants les AP au graphe de topologie
    for x in aps.values():
        topo.add_node(x.index, coord=x.coord, couleur=x.color, rayon=x.rayon, type=x.type_ap, groupe=x.groupe)

    #Ajout des arrets représentants l'interconnexion des AP
    for ap1 in aps.values():
        arrets = {}
        for ap2 in aps.values():
            if (ap1.index != ap2.index) and (ap1.index not in arrets.values()) and (ap1.IntersectionCouverture(ap2) == True):
                topo.add_edge(ap1.index, ap2.index)
                arrets[ap1.index] = ap2.index

    for u,v in topo.edges:
        topo[u][v]['poids'] = 1

    return topo


def affichage(graphe):

    #Création liste de couleurs pour affichage
    colors = []

    #Stockage des coordonnées et des couleurs dans des variables
    pos = nx.get_node_attributes(graphe,'coord')
    col = nx.get_node_attributes(graphe, 'couleur')
    ray = nx.get_node_attributes(graphe, 'rayon')
    poids = nx.get_edge_attributes(graphe, 'poids')

    #Ajout des couleurs dans la liste pour affichage
    for x in col:
        colors.append(col[x])

    #Affichage

    #Rayons de couverture
    fig, ax = plt.subplots()
    for n, xy in pos.items():
        cercle = pat.Circle(xy, ray[n], fill=False)
        ax.add_artist(cercle)


    #APs et Liens
    nx.draw_networkx_nodes(graphe, pos, node_color=colors, node_size=100)
    nx.draw_networkx_labels(graphe, pos, font_size=8)
    nx.draw_networkx_edges(graphe, pos)
    #nx.draw_networkx_edge_labels(graphe, pos, edge_labels = nx.get_edge_attributes(graphe, 'poids'))

    plt.savefig(f"Historique/graphe_{datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}.png", dpi=72)
    plt.show()

# def zones(topologie):
#     apcs = []
#     zones = ['yellow', 'green', 'violet', 'red', 'black']
#     i = 0
#     types = nx.get_node_attributes(topologie, 'type')
#     for noeud in types:
#         if types[noeud] == 'C':
#             apcs.append(noeud)

#     for apc in apcs:
#         dijkstra = dij.dijkstra(topologie, apc)
#         print(f"{apc}: {dijkstra}")
#         for noeud in dijkstra:
#             if dijkstra[noeud] >= 1 and dijkstra[noeud] < 20:
#                 topologie.nodes[noeud]['couleur'] = zones[i]
#                 topologie.nodes[noeud]['groupe'] = apc
#         i += 1
    
#     return topologie

def zones(topologie):
    apcs={}
    zones = {'isolé': []}
    couleurs_zones = ['white', 'green', 'violet', 'red', 'gray', 'yellow']
    i = 0
    types = nx.get_node_attributes(topologie, 'type')
    for noeud in types:
        if types[noeud] == 'C':
            apcs[noeud] = dij.dijkstra(topologie, noeud)
            zones[noeud] = []

    for noeud in topologie.nodes():
        min = math.inf
        zone = None
        for apc in apcs:
            if apcs[apc][noeud] < min and noeud not in apcs.keys():
                apcs[apc][noeud] = min
                zone = apc
        if zone != None:
            zones[zone].append(noeud)
            topologie.nodes[noeud]['groupe'] = zone
        else:
            zones['isolé'].append(noeud)
    
    print(zones)

    for zone in zones:
        for noeud in zones[zone]:
            topologie.nodes[noeud]['couleur'] = couleurs_zones[i]
        if zone != 'isolé':
            topologie.nodes[zone]['couleur'] = 'blue'
        i+=1

    return topologie

def degree(topologie):
    # Trouver le degré de chaque noeud
    degrees = topologie.degree()

    # Trier les degrés par ordre décroissant
    sorted_degrees = sorted(degrees.items(), key = lambda x:x[1], reverse = True)

    return sorted_degrees

def classify_nodes(graph):
    for node in graph.nodes():
        if len(list(graph.neighbors(node))) >= 2:
            graph.nodes[node]["type"] = "Relais"
        else:
            graph.nodes[node]["type"] = "Simple"

        

    

graphe = topologie()
affichage(graphe)
affichage(zones(graphe))






