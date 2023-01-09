import random as rd

def gen_ligne(nbr_lignes):
    aps = []
    apcs = []
    rayonAPC = 45
    rayonAP = 30
    for i in range(1, nbr_lignes+1):
        rayon = rd.choice([rayonAP, rayonAPC])
        if rayon == rayonAPC and len(apcs) < nbr_lignes//10:
            apcs.append(i)
        else:
            rayon = rayonAP
        ligne = f"{i} ({rd.randint(-100, 100)}, {rd.randint(-100, 100)}) {rayon}"
        aps.append(ligne)
    return aps, apcs

def gen_fichier(longeur):
    aps, apcs = gen_ligne(longeur)
    with open("Test/test_AP.txt", 'w') as f:
        for ap in aps:
            f.write(f'{ap}\n')

    with open("Test/test_APC.txt", 'w') as f:
        for apc in apcs:
            f.write(f"{apc} ")


gen_fichier(30)

