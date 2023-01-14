# Importation de tous les libraries nécéssaires, ainsi que le fichier ap.py pour la classe AP
import tkinter as tk
from tkinter import filedialog, Checkbutton
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import ap
import math

#-----------------------------------------------Affichage Tkinter-----------------------------------------------------

# Déclaration de variables globales (Fichiers d'entrée et liste pour les widgets)
FICHIER_AP = None
FICHIER_APC = None
WIDGETS = []

# Fonction d'importation pour le premier fichier (fichier AP)
def import_first_file():
    global FICHIER_AP
    FICHIER_AP = filedialog.askopenfilename()
    print(f"Fichier AP importé: {FICHIER_AP}")
    first_file_button.config(bg="green")

# Fonction d'importation pour le deuxième fichier (fichier APC)
def import_second_file():
    global FICHIER_APC
    FICHIER_APC = filedialog.askopenfilename()
    print(f"Fichier AP Contrôleur importé: {FICHIER_APC}")
    second_file_button.config(bg="green")

# Fonction pour démarrer le traitement des fichiers (Création de la topologie et détermination du type d'AP par zone)
def start():

    global topo
    # Réinitialisation des boutons et graphes
    Reinitialiser(WIDGETS)

    # Vérification que les fichiers sont bien importés
    if FICHIER_AP != None and FICHIER_APC != None:
        #Création de la topologie finale à l'aide des fonctions de traitement 
        topo = determination_type_AP(zones(topologie(FICHIER_AP, FICHIER_APC)))

        # Création de l'image d'aperçu  
        affichage(topo, "classique")
        image_topo = preview()
        image = Image.open(image_topo)
        image = ImageTk.PhotoImage(image)
        image_label.config(image=image)
        image_label.image = image
        plt.close()

        #Création des boutons qui peuvent agir sur la topologie

        # Bouton pour afficher la fenêtre de matplotlib
        plot_button = tk.Button(window, text="Afficher Plot", command=afficher_plot)
        plot_button.pack(padx=20, pady=20)
        WIDGETS.append(plot_button)

        # Bouton pour afficher les différents graphes représentants les différentes étapes du traitement
        detailles_button = tk.Button(window, text="Détailles", command=detailles)
        detailles_button.pack(padx=50, pady=20)
        WIDGETS.append(detailles_button)

        # Bouton pour afficher les AP Relais et leurs AP voisins
        ap_relais_button = tk.Button(window, text="Flux d'AP Relais", command=ap_relais)
        ap_relais_button.pack(padx=50, pady=20)
        WIDGETS.append(ap_relais_button)
    else:
        # Affichage d'erreur en cas de manque d'importation d'un de deux fichiers
        erreur = tk.Label(window, text="Importer les fichiers AP et APC avant de commencer")
        erreur.pack(padx=50, pady=50)
        WIDGETS.append(erreur)

# Fonction pour supprimer les widgets (boutons et labels)
def Reinitialiser(WIDGETS):
    for x in WIDGETS:
        x.pack_forget()

# Fonction pour le boutton ap_relais
def ap_relais():
    for deg in degree(topo):
        ap = tk.Label(window, text=f"L'AP n°{deg[0]} est relais pour {deg[1]} AP")
        ap.pack(padx=50, pady=1)

# Fonction pour le boutton afficher_plot
def afficher_plot():
    affichage(topo, "classique")
    plt.show()

# Fonction pour le boutton détailles
def detailles():
    graphe = topologie(FICHIER_AP, FICHIER_APC)
    affichage(graphe, "classique")
    plt.show()
    graphe2 = zones(graphe)
    affichage(graphe2, "arbre")
    plt.show()
    graphe3 = determination_type_AP(graphe2)
    affichage(graphe3, "classique")
    plt.show()

# Création de la fenêtre principale
window = tk.Tk()
window.title("Détermination du type d’AP Wifi, par zone")

# Création des boutons principales 

# Bouton pour importer le fichier AP
first_file_button = tk.Button(window, text="Importer coordonnées AP", command=import_first_file)
first_file_button.pack(padx=20, pady=20)

# Bouton pour importer le fichier APC
second_file_button = tk.Button(window, text="Importer AP Controller", command=import_second_file)
second_file_button.pack(padx=20, pady=20)

# Affichage de l'image d'aperçu 
image_label = tk.Label(window)
image_label.pack(side="right", fill="both", expand=True)

# Bouton pour démarrer le traitement
start_button = tk.Button(window, text="Start", command=start)
start_button.pack(padx=20, pady=20)


# Creation du footer et placement en bas à gauche
footer_label = tk.Label(window, text="Nicolas Egloff, Alexandro Amarayo, RT2A 2022/2023")
footer_label.pack(side="bottom")


#--------------------------------------TRAITEMENT-------------------------------------------------------------------

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

def topologie(AP, APC):

    #Création graphe représentant la topologie
    topo = nx.Graph()

    aps = ExtractionDesAP(AP, APC)
    arrets = {}

    #Ajout des sommets représentants les AP au graphe de topologie
    for x in aps.values():
        topo.add_node(x.index, coord=x.coord, couleur=x.color, rayon=x.rayon, type=x.type_ap, zone=x.zone)

    #Ajout des arrets représentants l'interconnexion des AP
    for ap1 in aps.values():
        arrets = {}
        for ap2 in aps.values():
            if (ap1.index != ap2.index) and (ap1.index not in arrets.values()) and (ap1.IntersectionCouverture(ap2) == True):
                topo.add_edge(ap1.index, ap2.index)
                topo[ap1.index][ap2.index]['poids'] = ap1.DistanceEntreAP(ap2)
                arrets[ap1.index] = ap2.index

    return topo

def affichage(graphe, option):

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

    #APs et Liens
    nx.draw_networkx_nodes(graphe, pos, node_color=colors, node_size=100)
    nx.draw_networkx_labels(graphe, pos, font_size=8)
    if option == "classique":
        AffichageCercles(graphe, pos, ray)
    elif option == "arbre":
        nx.draw_networkx_edges(graphe, pos)
    elif option == "arbre_cout":
        nx.draw_networkx_edge_labels(graphe, pos, edge_labels = nx.get_edge_attributes(graphe, 'poids'))

    plt.savefig(f"Historique/graphe_{datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}.png", dpi=72)

def AffichageCercles(graphe, pos, ray):

    couleurs_cercles = {}
    for noeud in graphe.nodes():
        if graphe.nodes[noeud]['type'] == 'R':
            couleurs_cercles[noeud] = 'green'
        elif graphe.nodes[noeud]['type'] == 'S':
            couleurs_cercles[noeud] = 'red'
        elif graphe.nodes[noeud]['type'] == 'C':
            couleurs_cercles[noeud] = 'blue'
        else:
            couleurs_cercles[noeud] = 'gray'
        if graphe.nodes[noeud]['zone'] == 'isolé':
            couleurs_cercles[noeud] = '#00000000'

    ax = plt.gca()
    min_x = 0
    max_x = 0

    min_y = 0
    max_y = 0

    max_rayon = 0

    for n, xy in pos.items():
        if (xy[0] > max_x):
            max_x = xy[0]
        if (xy[0] < min_x):
            min_x = xy[0]

        if (xy[1] > max_y):
            max_y = xy[1]
        if (xy[1] < min_y):
            min_y = xy[1]

        for rayon in ray.values():
            if rayon > max_rayon:
                max_rayon=rayon
                
        cercle = plt.Circle(xy, ray[n], fill=False, color=couleurs_cercles[n])
        ax.add_artist(cercle)
    
    ax.set_aspect(1)
    ax.set(xlim=(min_x-max_rayon, max_x+max_rayon+80), ylim=(min_y-max_rayon, max_y+max_rayon))

    line1 = plt.Line2D([], [], color="white", marker='o', markersize=12, markerfacecolor="white", markeredgecolor="blue")
    line2 = plt.Line2D([], [], color="white", marker='o', markersize=12, markerfacecolor="white", markeredgecolor="red")
    line3 = plt.Line2D([], [], color="white", marker='o', markersize=12,  markerfacecolor="white", markeredgecolor="green")
    line4 = plt.Line2D([], [], color="white", marker='o', markersize=12, markerfacecolor="white", markeredgecolor="white")
    plt.legend((line1, line2, line3, line4), ('Controlêur', 'Simple', 'Relais', 'Isolé'), numpoints=1, loc='lower right', title="Type d'AP")

def preview():
    titre = f"graphe_{datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}.png"
    plt.savefig(titre, dpi=72)

    return titre

def zones(topologie):
    apcs={}
    pred={}
    zones = {'isolé': []}
    couleurs_zones = ['white', 'green', 'violet', 'red', 'gray', 'yellow']
    i = 0
    types = nx.get_node_attributes(topologie, 'type')

    for noeud in types:
        if types[noeud] == 'C':
            apcs[noeud], pred[noeud] = dijkstra(topologie, noeud)
            zones[noeud] = []

    topologie_zones = nx.create_empty_copy(topologie)

    for noeud in topologie_zones.nodes():
        min = math.inf
        zone = None
        for apc in apcs:
            if apcs[apc][noeud] < min:
                min = apcs[apc][noeud]
                zone = apc
        if zone != None:
            zones[zone].append(noeud)
            topologie_zones.nodes[noeud]['zone'] = zone
        else:
            zones['isolé'].append(noeud)
            topologie_zones.nodes[noeud]['zone'] = 'isolé'
    
    print(zones)

    for zone in zones:
        for noeud in zones[zone]:
            topologie_zones.nodes[noeud]['couleur'] = couleurs_zones[i]
            if zone != 'isolé':
                if pred[zone][noeud] != None:
                    topologie_zones.add_edge(noeud, pred[zone][noeud], poids=apcs[zone][noeud])
        if zone != 'isolé':
            topologie_zones.nodes[zone]['couleur'] = 'blue'
        i+=1

    return topologie_zones
        
def degree(topologie):
    ap_relais = []

    # Trouver le degré de chaque noeud
    degrees = topologie.degree()

    # Trier les degrés par ordre décroissant
    sorted_degrees = sorted(degrees, key = lambda x:x[1], reverse = True)

    for deg in sorted_degrees:
        if topologie.nodes[deg[0]]['type'] == "R":
            ap_relais.append(deg)                                                                                                                                                                                                                                                                                                                                                                                   

    return ap_relais

def determination_type_AP(graph):
    for noeud in graph.nodes():
        voisins_zones = voisins_de_zone(graph, noeud)
        if graph.nodes[noeud]['type'] != "C":
            if voisins_zones >= 2:
                graph.nodes[noeud]["type"] = "R"
            else:
                graph.nodes[noeud]["type"] = "S"
    
    return graph

def voisins_de_zone(graph, noeud):
    voisins = 0
    for voisin in graph.neighbors(noeud):
        if graph.nodes[voisin]['zone'] == graph.nodes[noeud]['zone']:
            voisins += 1
    
    return voisins
            
def couleurs_types(graph):
    couleurs = {}
    for noeud in graph.nodes():
        if graph.nodes[noeud]['type'] == 'R':
            couleurs[noeud] = 'green'
        elif graph.nodes[noeud]['type'] == 'S':
            couleurs[noeud] = 'red'
        elif graph.nodes[noeud]['type'] == 'C':
            couleurs[noeud] = 'blue'
        else:
            couleurs[noeud] = 'gray'
        if graph.nodes[noeud]['zone'] == 'isolé':
            couleurs[noeud] = '#00000000'

    print(nx.get_node_attributes(graph, 'zone'))
    return couleurs

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
    
    return distances, predeceseurs

# Démarrage de l'application  
if __name__=="__main__":
    # Lancer la boucle principale de Tkinter
    window.mainloop()



