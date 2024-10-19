from Personne import Personne

class Seigneur(Personne):
    def __init__(self, nom, prenom, age, edv, bonheur, argent, couleur) -> None:
        super().__init__(nom, prenom, age, edv, bonheur, argent)
        self._couleur = couleur

    # Getter pour couleur
    @property
    def couleur(self):
        return self._couleur

    # Setter pour couleur
    @couleur.setter
    def couleur(self, value): 
        self._couleur = value
