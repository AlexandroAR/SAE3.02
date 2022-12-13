class AP():
    def __init__(self, index=0, coord=(0, 0) , rayon=0, color='white', type_ap = 'S'):
        self.index = index
        self.coord = coord
        self.rayon = rayon
        self.color = color
        self.type_ap = type_ap

    def __str__(self):
        return f"AP n°{self.index}\nCoordonnées: {self.coord}\nRayon de coverture: {self.rayon}\nCouleur: {self.color}\nType: {self.type_ap}"
