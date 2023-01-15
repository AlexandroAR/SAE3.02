import math

class AP():
    # Initialisation de toutes les variables
    def __init__(self, index=0, coord=(0, 0) , rayon=0, color='white', type_ap = 'S', zone=None):
        self.index = index
        self.coord = coord
        self.rayon = rayon
        self.color = color
        self.type_ap = type_ap
        self.zone = zone

    # Affiche les attributs de l'objet
    def __str__(self):
        return f"AP n°{self.index}\nCoordonnées: {self.coord}\nRayon de coverture: {self.rayon}\nCouleur: {self.color}\nType: {self.type_ap}"

    # Calcule la distance entre une AP distante et lui-même
    def DistanceEntreAP(self, ap):
        return math.sqrt((self.coord[0]-ap.coord[0])**2 + (self.coord[1]-ap.coord[1])**2)

    # Vérifie si le centre de l'AP distant est dedans son rayon de couverture
    def IntersectionCouverture(self, ap):
        distanceCentres = self.DistanceEntreAP(ap)

        if distanceCentres <= max(self.rayon, ap.rayon):
            return True
        
        return False