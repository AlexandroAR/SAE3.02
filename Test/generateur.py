import random as rd

def gen_ligne(nbr_lignes):
    aps = []
    for i in range(1, nbr_lignes+1):
        ligne = f"{i} ({rd.randint(-200, 200)}, {rd.randint(-200, 200)}) {rd.randint(10, 30)}"
        aps.append(ligne)
    return aps

def gen_fichier(longeur):
    aps = gen_ligne(longeur)
    with open("test_AP.txt", 'w') as f:
        for ap in aps:
            f.write(f'{ap}\n')

    with open("test_APC.txt", 'w') as f:
        for x in range(0, (len(aps)//10)):
            apc = rd.randint(1, len(aps))
            f.write(f"{apc} ")


gen_fichier(50)


