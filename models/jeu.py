import json


class Jeu:
    def __init__(self, nom, categorie, annee, joueursmin, joueursmax, age, duree, disponible):
        self.categorie = categorie
        self.nom = nom
        self.annee = annee
        self.joueursmin = joueursmin
        self.joueursmax = joueursmax
        self.age = age
        self.duree = duree
        self.disponible = disponible

    def __repr__(self) -> str:
        return self.categorie + ": " + self.nom + ", " + str(self.annee) + ", " + str(self.joueursmin) + " à " + str(self.joueursmax) + ", " + str(self.age) + ", " + self.duree + ", " + ("diposnible" if self.disponible == "True" else "indisponible")
    # 10.	Stratégie: « Agricola », Z-Man Games, 2007,  1-4 joueurs, 12+, 30-150 minutes

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
