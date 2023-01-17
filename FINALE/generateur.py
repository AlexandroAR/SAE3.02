import random as rd

def gen_lignes(nbr_lignes):
    # Liste des AP et des AP contrôleurs pour ajouter les différentes lignes des fichiers
    aps = []
    apcs = []
    # Rayons des AP
    rayonAPC = 45
    rayonAP = 30

    # Génére aléatoirement une position et génére 1 AP contrôleur pour 10 AP
    for i in range(1, nbr_lignes+1):
        rayon = rd.choice([rayonAP, rayonAPC])
        if rayon == rayonAPC and len(apcs) < nbr_lignes//10:
            apcs.append(i)
        else:
            rayon = rayonAP
        ligne = f"{i} ({rd.randint(-100, 100)}, {rd.randint(-100, 100)}) {rayon}"
        aps.append(ligne)
    return aps, apcs

# Parcours les liste aps et apcs et écrit les lignes sur les fichiers test_AP et test_APC
def gen_fichier(longeur):
    aps, apcs = gen_lignes(longeur)
    with open("test_AP.txt", 'w') as f:
        for ap in aps:
            f.write(f'{ap}\n')

    with open("test_APC.txt", 'w') as f:
        for apc in apcs:
            f.write(f"{apc} ")


gen_fichier(40)

