class AP():
    def __init__(self, index=0, coord=(0, 0) , rayon=0):
        self.index = index
        self.coord = coord
        self.rayon = rayon

    def __str__(self):
        return f"AP n°{self.index}\nCoordonnées: {self.coord}\nRayon de coverture: {self.rayon}"
