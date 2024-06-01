from flask_login import UserMixin
from .jeu import Jeu
import json


class User(UserMixin):
    def __init__(self, email, name, password, id, jeux) -> None:
        self.email = email
        self.name = name
        self.password = password
        self.id = id
        self.jeux = jeux


def recuperer_uilisateur(id) -> User:
    with open("./db/utilisateurs.json", "r") as f:
        utilisateursData = json.load(f)
        for utilisateurData in utilisateursData:
            if int(utilisateurData["id"]) == int(id):
                return User(utilisateurData["email"], utilisateurData["name"], utilisateurData["password"], id, [Jeu(
                    jeu["nom"], jeu["categorie"], jeu["annee"], jeu["joueursmin"], jeu["joueursmax"], jeu["age"], jeu["duree"], jeu["disponible"]) for jeu in utilisateurData["jeux"]])

    return None
