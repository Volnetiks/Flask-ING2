from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from .models.user import User
from .models.jeu import Jeu
import json

main = Blueprint('main', __name__)


@main.route("/")
def index():
    jeux = []
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            if jeuData["disponible"] == "True":
                jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                                jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))

    return render_template("index.html", jeux=jeux)


@main.route("/recherche", methods=["POST"])
def recherche():
    value = request.form.get("recherche")
    jeux = []
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            if value.lower() in jeuData["nom"].lower() or value.lower() in jeuData["categorie"].lower():
                jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                                jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))
            elif value.isnumeric():
                if jeuData["annee"] == int(value) or (jeuData["joueursmin"] < int(value) and jeuData["joueursmax"] > int(value)) or (jeuData["age"] < int(value) and int(value) < 100):
                    jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                                jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))

    return render_template('recherche.html', jeux=jeux, value=value)


@main.route("/recherche")
def recherche_tout():
    jeux = []
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                            jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))

    return render_template('recherche.html', jeux=jeux)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name, jeux=current_user.jeux)


@main.route("/reservation")
@login_required
def reservation():
    jeux = []
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            if jeuData["disponible"] == "True":
                jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                                jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))

    return render_template("reservation.html", jeux=jeux)


@main.route("/reservation_confirmation/<nom>")
@login_required
def reservation_confirmation(nom):
    jeu = None
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            if jeuData["nom"] == nom:
                jeu = Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                          jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"])

    return render_template("reservation_confirmation.html", jeu=jeu)


@main.route("/retour_confirmation/<nom>")
@login_required
def retour_confirmation(nom):
    jeu = None
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            if jeuData["nom"] == nom:
                jeu = Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                          jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"])

    return render_template("retour_confirmation.html", jeu=jeu)


@main.route("/reservation_confirmation/<nom>", methods=["POST"])
@login_required
def reservation_confirmation_post(nom):
    jeux = []
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                            jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))

    jeu = next(j for j, v in enumerate(jeux) if v.nom == nom)
    jeux[jeu].disponible = "False"
    with open("./db/jeux.json", "w") as f:
        json.dump(jeux, f, indent=4, default=obj_dict)
    utilisateurs = []
    with open("./db/utilisateurs.json", "r") as f:
        utilisateursData = json.load(f)
        for utilisateurData in utilisateursData:
            utilisateurs.append(User(utilisateurData["email"], utilisateurData["name"], utilisateurData["password"], utilisateurData["id"], [Jeu(
                jeu["nom"], jeu["categorie"], jeu["annee"], jeu["joueursmin"], jeu["joueursmax"], jeu["age"], jeu["duree"], jeu["disponible"]) for jeu in utilisateurData["jeux"]]))

    indexUser = next(u for u, v in enumerate(utilisateurs)
                     if v.name == current_user.name)
    utilisateurs[indexUser].jeux.append(jeux[jeu])

    with open("./db/utilisateurs.json", "w") as f:
        json.dump(utilisateurs, f, indent=4, default=obj_dict)

    return redirect(url_for("main.profile"))


@main.route("/retour_confirmation/<nom>", methods=["POST"])
@login_required
def retour_confirmation_post(nom):
    jeux = []
    with open("./db/jeux.json", "r") as f:
        jeuxData = json.load(f)
        for jeuData in jeuxData:
            jeux.append(Jeu(jeuData["nom"], jeuData["categorie"], jeuData["annee"], jeuData["joueursmin"],
                            jeuData["joueursmax"], jeuData["age"], jeuData["duree"], jeuData["disponible"]))

    jeu = next(j for j, v in enumerate(jeux) if v.nom == nom)
    jeux[jeu].disponible = "True"
    with open("./db/jeux.json", "w") as f:
        json.dump(jeux, f, indent=4, default=obj_dict)

    utilisateurs = []
    with open("./db/utilisateurs.json", "r") as f:
        utilisateursData = json.load(f)
        for utilisateurData in utilisateursData:
            utilisateurs.append(User(utilisateurData["email"], utilisateurData["name"], utilisateurData["password"], utilisateurData["id"], [Jeu(
                jeu["nom"], jeu["categorie"], jeu["annee"], jeu["joueursmin"], jeu["joueursmax"], jeu["age"], jeu["duree"], jeu["disponible"]) for jeu in utilisateurData["jeux"]]))

    indexUser = next(u for u, v in enumerate(utilisateurs)
                     if v.name == current_user.name)
    indexJeu = next(j for j, v in enumerate(
        utilisateurs[indexUser].jeux) if v.nom == nom)
    utilisateurs[indexUser].jeux.pop(indexJeu)

    with open("./db/utilisateurs.json", "w") as f:
        json.dump(utilisateurs, f, indent=4, default=obj_dict)

    return redirect(url_for("main.profile"))


def obj_dict(obj):
    return obj.__dict__
