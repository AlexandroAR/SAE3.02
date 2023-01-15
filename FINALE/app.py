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

# Fonction pour générer une liste d'objets AP à partir des fichiers d'entrée
def ExtractionDesAP(fichier_ap, fichier_apc):

    # Liste et dictionnaire des AP et AP controlêurs
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
        # Découpage de la ligne en parties
        x = x.strip().split(' ')

        # Extraction de l'index
        index = x[0].strip()

        # Extraction du rayon
        rayon = x[3].strip()

        # Extraction des coordonnées dans tuple coord
        coord = (x[1][1:x[1].find(',')], x[2][:x[2].find(')')])
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

# Création de la topologie sur networkx à partir des fichiers d'entrée
def topologie(AP, APC):

    #Création d'un graphe représentant la topologie
    topo = nx.Graph()

    # Création d'un dictionnaire contenant les AP et un autre pour ajouter les arrêts
    aps = ExtractionDesAP(AP, APC)
    arrets = {}

    # Ajout des sommets représentants les AP au graphe de topologie
    for x in aps.values():
        topo.add_node(x.index, coord=x.coord, couleur=x.color, rayon=x.rayon, type=x.type_ap, zone=x.zone)

    # Ajout des arrets représentants l'interconnexion des AP avec le poids représentant la distance euclidienne
    for ap1 in aps.values():
        arrets = {}
        for ap2 in aps.values():
            if (ap1.index != ap2.index) and (ap1.index not in arrets.values()) and (ap1.IntersectionCouverture(ap2) == True):
                topo.add_edge(ap1.index, ap2.index)
                topo[ap1.index][ap2.index]['poids'] = ap1.DistanceEntreAP(ap2)
                arrets[ap1.index] = ap2.index

    return topo

# Fonction pour afficher la topologie des différentes manières (selon l'option) avec matplotlib 
def affichage(graphe, option):

    #Stockage des différents attributs des noeuds et arrêts dans des variables
    pos = nx.get_node_attributes(graphe,'coord')
    col = nx.get_node_attributes(graphe, 'couleur')
    ray = nx.get_node_attributes(graphe, 'rayon')
    poids = nx.get_edge_attributes(graphe, 'poids')

    # Traduit le dictionnaire de couleurs des AP à une liste de couleurs
    # Création liste de couleurs des AP pour l'affichage
    colors = []
    # Ajout des couleurs dans la liste pour affichage
    for x in col:
        colors.append(col[x])

    #Affichage

    #APs (noeuds)
    nx.draw_networkx_nodes(graphe, pos, node_color=colors, node_size=100)
    nx.draw_networkx_labels(graphe, pos, font_size=8)

    # Affichage d'une topologie avec APs (noeuds) et leurs rayons de couverture (cercles)
    if option == "classique":
        AffichageCercles(graphe, pos, ray)
    # Affichage d'une topologie avec des APs (noeuds) et leurs connexions (de préférance à l'utiliser pour des zones représentés par des arbres) 
    elif option == "arbre":
        nx.draw_networkx_edges(graphe, pos)
    # Même affichage que la topologie 'arbre' mais les connexions (arrêts) sont représentés par les distances (poids) entre les AP 
    elif option == "arbre_cout":
        nx.draw_networkx_edge_labels(graphe, pos, edge_labels = nx.get_edge_attributes(graphe, 'poids'))

# Fonction auxiliaire à affichage pour afficher les rayons de couverture (cercles) des AP 
def AffichageCercles(graphe, pos, ray):
    # Dictionnaires pour ajouter les couleurs de chaque rayon de couverture de chaque AP
    couleurs_cercles = {}

    # Parcours des AP (noeuds) et ajout de couleur à leurs rayons de couverutre selon le type d'AP
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

    # Variables nécéssaires pour l'affichage des cercles
    ax = plt.gca()
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    max_rayon = 0

    # Parcours des noeuds et leurs positions
    for n, xy in pos.items():
        # Détermination des coordonnées maximales et minimales des AP
        if (xy[0] > max_x):
            max_x = xy[0]
        if (xy[0] < min_x):
            min_x = xy[0]
        if (xy[1] > max_y):
            max_y = xy[1]
        if (xy[1] < min_y):
            min_y = xy[1]

        #Détérmination du rayon maximal
        for rayon in ray.values():
            if rayon > max_rayon:
                max_rayon=rayon

        # Création d'un cercle avec sa position et sa couleur respective (affichage)  
        cercle = plt.Circle(xy, ray[n], fill=False, color=couleurs_cercles[n])
        ax.add_artist(cercle)
    
    # Configuration des axes pour la fenêtre d'affichage
    ax.set_aspect(1)
    ax.set(xlim=(min_x-max_rayon, max_x+max_rayon+80), ylim=(min_y-max_rayon, max_y+max_rayon))

    # Légende pour les cercles (type d'AP)
    line1 = plt.Line2D([], [], color="white", marker='o', markersize=12, markerfacecolor="white", markeredgecolor="blue")
    line2 = plt.Line2D([], [], color="white", marker='o', markersize=12, markerfacecolor="white", markeredgecolor="red")
    line3 = plt.Line2D([], [], color="white", marker='o', markersize=12,  markerfacecolor="white", markeredgecolor="green")
    line4 = plt.Line2D([], [], color="white", marker='o', markersize=12, markerfacecolor="white", markeredgecolor="white")
    plt.legend((line1, line2, line3, line4), ('Controlêur', 'Simple', 'Relais', 'Isolé'), numpoints=1, loc='lower right', title="Type d'AP")

# Génère l'image pour l'aperçu du graphe
def preview():
    titre = f"graphe_{datetime.datetime.today().strftime('%d-%m-%Y_%H-%M-%S')}.png"
    plt.savefig(titre, dpi=72)

    return titre

# Crée une nouvelle topologie avec les différentes zones représentés par des arbres couvrants 
def zones(topologie):
    # Dictionnaires pour les listes de distances, prédécesseurs et zones de chaque AP Contrôleur
    apcs={}
    pred={}
    zones = {'isolé': []}

    # Variables auxiliaires
    couleurs_zones = ['white', 'green', 'violet', 'red', 'gray', 'yellow']
    i = 0
    types = nx.get_node_attributes(topologie, 'type')

    # Ajout des listes de distances et des prédécesseurs de chaque AP Contrôleur à partir de la fonction dijkstra
    for noeud in types:
        if types[noeud] == 'C':
            apcs[noeud], pred[noeud] = dijkstra(topologie, noeud)
            zones[noeud] = []

    # Copie de la topologie sans les arrêts
    topologie_zones = nx.create_empty_copy(topologie)

    # Distribution des AP par zone à partir des listes de distances des AP Contrôleurs
    for noeud in topologie_zones.nodes():
        min = math.inf
        zone = None
        # Prend l'AP Contrôleur le plus proche du noeud
        for apc in apcs:
            if apcs[apc][noeud] < min:
                min = apcs[apc][noeud]
                zone = apc
        # Ajout du noeud à la zone correspondante à l'AP Contrôleur ou à la zone 'isolé'
        if zone != None:
            zones[zone].append(noeud)
            topologie_zones.nodes[noeud]['zone'] = zone
        else:
            zones['isolé'].append(noeud)
            topologie_zones.nodes[noeud]['zone'] = 'isolé'
    
    print(zones)

    # Attribution des couleurs selon la zone et création des arbres couvrants par zone
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

# Renvoie les degrées des AP relais en ordre décroissant    
def degree(topologie):
    ap_relais = []

    # Trouver le degré de chaque noeud
    degrees = topologie.degree()

    # Trier les degrés par ordre décroissant
    sorted_degrees = sorted(degrees, key = lambda x:x[1], reverse = True)

    # Ajouter uniquement les degrés des AP relais dans une liste 
    for deg in sorted_degrees:
        if topologie.nodes[deg[0]]['type'] == "R":
            ap_relais.append(deg)                                                                                                                                                                                                                                                                                                                                                                                   

    return ap_relais

# Détermine le type d'AP
def determination_type_AP(graphe):
    # Détermine si l'AP est un relais ou non en se basant sur le nombre de ses voisins de zone 
    for noeud in graphe.nodes():
        voisins_zones = voisins_de_zone(graphe, noeud)
        if graphe.nodes[noeud]['type'] != "C":
            if voisins_zones >= 2:
                graphe.nodes[noeud]["type"] = "R"
            else:
                graphe.nodes[noeud]["type"] = "S"
    
    return graphe

# Détermine le nombre de voisins qui appartiennent à la zone du noeud
def voisins_de_zone(graphe, noeud):
    voisins = 0
    for voisin in graphe.neighbors(noeud):
        if graphe.nodes[voisin]['zone'] == graphe.nodes[noeud]['zone']:
            voisins += 1
    
    return voisins

# Fonction de qui calcule les distances les plus courtes entre un noeud E et le reste des noeuds du graphe avec l'algorithme de Dijkstra  
def dijkstra(graphe, E):
    # Déclaration des dictionnaires et de la queue de traitement
    queue, distances, predecesseurs = [], {}, {}

    # Initialisation des distances et des prédécesseurs et ajout de tous les noeuds à la queue de traitement
    for noeud in graphe.nodes:
        queue.append(noeud)
        distances[noeud] = math.inf
        predecesseurs[noeud] = None

    # Distance du noeud E au noeud E mis à 0
    distances[E] = 0

    # Traitement jusqu'à qu'il n'y a plus de noeuds dans la queue à traiter
    while len(queue) > 0:
        min = math.inf
        # Prend le noeud dans la queue avec la distance la plus petite distance
        for S in queue:
            if distances[S] < min:
                min = distances[S]
                u = S
              
        if u in queue:
            queue.remove(u)
            # Pour chaque voisin du noeud en traitement (u) on attribut une nouvelle distance si celle-ci est plus petite que la distance actuelle du voisin v et on ajoute son prédécéseur au noeud u
            for v in graphe.neighbors(u):
                if v in queue:
                    dist = distances[u] + graphe[u][v]['poids']
                    if dist < distances[v]:
                        distances[v] = dist
                        predecesseurs[v] = u
        else:
            break
    
    return distances, predecesseurs

# Démarrage de l'application  
if __name__=="__main__":
    # Lance la boucle principale de Tkinter
    window.mainloop()
