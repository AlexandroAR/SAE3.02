import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import datetime
import ap
import dijkstra as dij
import math


def ExtractionDesAP(fichier_ap, fichier_apc):
    # Liste et dictionnaire des AP et AP controleurs
    aps = {}
    apcs = []

    # Extraction des lignes (APs) dans une liste
    with open(fichier_ap, 'r') as f:
        lignes = f.readlines()

    # Création de liste d'index des AP controleurs
    with open(fichier_apc, 'r') as f:
        apcs = f.readline().strip().split(' ')

    # Boucle de création des AP
    for x in lignes:
        x.strip()

        # Extraction de l'index (2 premiers caractères)
        index = x[:2].strip()

        # Extraction du rayon (2 derniers caractères)
        rayon = x[-4:].strip()

        # Extraction des coordonnées dans tuple coord
        coord = x[x.find('(') + 1:x.find(')')]
        coord = coord.split(",")
        coord = (int(coord[0]), int(coord[1]))

        # Triage de mode et couleur de AP
        if index in apcs:
            couleur = 'blue'
            type_ap = 'C'
        else:
            couleur = 'gray'
            type_ap = 'S'

        # Création d'un objet AP et ajout en dictionnaire des AP
        a = ap.AP(index, coord, int(rayon), couleur, type_ap)
        aps[index] = a
        print(a)

    return aps


def topologie():
    # Création graphe représentant la topologie
    topo = nx.Graph()

    aps = ExtractionDesAP("Test/test_AP.txt", "Test/test_APC.txt")
    arrets = {}

    # Ajout des sommets représentants les AP au graphe de topologie
    for x in aps.values():
        topo.add_node(x.index, coord = x.coord, couleur = x.color, rayon = x.rayon, type = x.type_ap, groupe = x.groupe)

    # Ajout des arrets représentants l'interconnexion des AP
    for ap1 in aps.values():
        arrets = {}
        for ap2 in aps.values():
            if (ap1.index != ap2.index) and (ap1.index not in arrets.values()) and (
                    ap1.IntersectionCouverture(ap2) == True):
                topo.add_edge(ap1.index, ap2.index)
                topo[ap1.index][ap2.index]['poids'] = ap1.DistanceEntreAP(ap2)
                arrets[ap1.index] = ap2.index

    # for u,v in topo.edges:
    #     topo[u][v]['poids'] = 1

    return topo


def affichage(graphe):
    # Création liste de couleurs pour affichage
    colors = []

    # Stockage des coordonnées et des couleurs dans des variables
    pos = nx.get_node_attributes(graphe, 'coord')
    col = nx.get_node_attributes(graphe, 'couleur')
    ray = nx.get_node_attributes(graphe, 'rayon')
    poids = nx.get_edge_attributes(graphe, 'poids')

    # Ajout des couleurs dans la liste pour affichage
    for x in col:
        colors.append(col[x])

    # Affichage

    # Rayons de couverture
    fig, ax = plt.subplots()
    for n, xy in pos.items():
        cercle = pat.Circle(xy, ray[n], fill = False)
        ax.add_artist(cercle)

    # APs et Liens
    nx.draw_networkx_nodes(graphe, pos, node_color = colors, node_size = 100)
    nx.draw_networkx_labels(graphe, pos, font_size = 8)
    nx.draw_networkx_edges(graphe, pos)
    # nx.draw_networkx_edge_labels(graphe, pos, edge_labels = nx.get_edge_attributes(graphe, 'poids'))

    plt.savefig(f"Historique/graphe_{datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}.png", dpi = 72)
    plt.show()


def zones(topologie):
    # Initialisation des dictionnaires et listes vides
    apcs = {}
    zones = {'isolé':[]}
    couleurs_zones = ['blanc', 'vert', 'violet', 'rouge', 'gris', 'jaune']
    i = 0

    # Récupère un dictionnaire de nœuds et de leurs attributs 'type'
    types = nx.get_node_attributes(topologie, 'type')

    # Parcoure tous les nœuds du réseau
    for noeud in types:
        if types[noeud] == 'C':
            # Si un nœud a un attribut 'type' avec la valeur 'C', l'ajouter au dictionnaire "apcs"
            apcs[noeud] = dij.dijkstra(topologie, noeud)
            # Et créer une nouvelle clé dans le dictionnaire "zones" avec le même nom que le nœud
            zones[noeud] = []

    # Parcours tous les nœuds de la topologie
    for noeud in topologie.nodes():
        min = math.inf
        zone = None
        # Pour chaque nœud, trouver l'APC à la distance la plus courte
        for apc in apcs:
            if apcs[apc][noeud] < min and noeud not in apcs.keys():
                min = apcs[apc][noeud]
                zone = apc
        # Assigne la zone au nœud et stocke le nœud dans la liste de zone
        if zone != None:
            zones[zone].append(noeud)
            topologie.nodes[noeud]['groupe'] = zone
        else:
            zones['isolé'].append(noeud)

    # Affiche le dictionnaire des zones
    print(zones)

    # Parcours toutes les zones, et tous les nœuds dans chaque zone
    for zone in zones:
        for noeud in zones[zone]:
            # Assigne la couleur de la liste "couleurs_zones" au nœud
            topologie.nodes[noeud]['couleur'] = couleurs_zones[i]
        # Si la zone est un APC, la colore en bleu
        if zone != 'isolé':
            topologie.nodes[zone]['couleur'] = 'bleu'
        i += 1

    # Renvoie la topologie modifiée
    return topologie


def degree(topologie):
    # Trouver le degré de chaque noeud
    degrees = topologie.degree()

    # Trier les degrés par ordre décroissant
    sorted_degrees = sorted(degrees, key = lambda x:x[1], reverse = True)

    return sorted_degrees


def classify_nodes(graph):
    # Parcours tous les nœuds du graphe
    for node in graph.nodes():
        # Vérifie si le nœud a au moins deux voisins
        if len(list(graph.neighbors(node))) >= 2:
            # Si oui, affecte le type "Relais" au nœud
            graph.nodes[node]["type"] = "Relais"
        else:
            # Sinon, affecte le type "Simple" au nœud
            graph.nodes[node]["type"] = "Simple"

graphe = topologie()
affichage(graphe)
affichage(zones(graphe))
