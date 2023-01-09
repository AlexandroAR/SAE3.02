import math

class AP():
    def __init__(self, index=0, coord=(0, 0) , rayon=0, color='white', type_ap = 'S', groupe=0):
        self.index = index
        self.coord = coord
        self.rayon = rayon
        self.color = color
        self.type_ap = type_ap
        self.groupe = groupe

    def __str__(self):
        return f"AP n°{self.index}\nCoordonnées: {self.coord}\nRayon de coverture: {self.rayon}\nCouleur: {self.color}\nType: {self.type_ap}"

    def IntersectionCouverture(self, ap):
        distanceCentres = math.sqrt((self.coord[0]-ap.coord[0])**2 + (self.coord[1]-ap.coord[1])**2) 
        


        if distanceCentres <= max(self.rayon, ap.rayon):
            return True
        
        return False