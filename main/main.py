import networkx as nx
import matplotlib.pyplot as plt
import ap

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
            couleur = 'red'
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
        topo.add_node(x.index, coord=x.coord, couleur=x.color)

    #Ajout des arrets représentants l'interconnexion des AP
    for ap1 in aps.values():
        for ap2 in aps.values():
            if (ap1.index != ap2.index) and (ap1.index not in arrets.values()) and (ap1.IntersectionCouverture(ap2) == True):
                topo.add_edge(ap1.index, ap2.index)
                arrets[ap1.index] = ap2.index

    print(arrets)

    return topo


def affichage(graphe):

    #Création liste de couleurs pour affichage
    colors = []

    #Stockage des coordonnées et des couleurs dans des variables
    pos = nx.get_node_attributes(graphe,'coord')
    col = nx.get_node_attributes(graphe, 'couleur')

    #Ajout des couleurs dans la liste pour affichage
    for x in col:
        colors.append(col[x])

    #Affichage
    nx.draw_networkx_nodes(graphe, pos, node_color=colors)
    nx.draw_networkx_labels(graphe, pos)
    nx.draw_networkx_edges(graphe, pos)
    plt.show()

affichage(topologie())





