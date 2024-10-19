class Personne:
    def __init__(self, nom, prenom, age, edv, bonheur, argent) -> None:
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.edv = edv
        self.bonheur= bonheur
        self.argent = argent
    

    def incr_age(self, nb):
        self.age+=nb

    def __str__(self) -> str:
        return f'je suis {self.nom} {self.prenom}, j ai {self.age} je vais vivre jusqu a {self.edv}'