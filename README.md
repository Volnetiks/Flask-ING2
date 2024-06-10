# Ludothèque ING2

## Description
Le projet de ludothèque à permis de mettre en commun toutes les connaissances apprises lors des années de cycle préparatoire (SQL, Python, HTML/CSS)

## Table des Matières
1. [Installation](#installation)
2. [Usage](#usage)
3. [Fonctionnalités](#fonctionnalités)
4. [Licence](#licence)

## Installation
L'installation du projet se fait via le fichier **installer.cmd**. Ce fichier se charge d'installer de configurer l'entiereté du projet.
Le projet peut également être configurer à la main
```bash
# Clone ce dépôt
git clone https://github.com/Volnetiks/Flask-ING2 "Ludothèque - Thomas, Etienne, Benjamin, Antoine, Delvin"

# Navigue dans le dossier du projet
cd "Ludothèque - Thomas, Etienne, Benjamin, Antoine, Delvin"

# Configure l'environnement
py -m venv env

# Active l'environnement python
.\env\Sources\activate

# Installe les dépendences nécessaire
pip install flask flask_login psycopg2
```

## Usage
**Veuillez noter que le projet ne se lancera que sur des réseaux supportant l'IPv6 (le réseau ESAIP ne fonctionnera pas)

Le projet peut-être lancer via **start.bat** ou bien en ligne de commandes.
```bash
# Lance l'environnement python
.\env\Sources\activate

# Lance le projet
flask --app __init__ run --debug
```

Vous pouvez ensuite accéder au projet via l'url 127.0.0.1:5000

## Fonctionnalités
Liste des principales fonctionnalités du projet:
- Création de compte
- Système de connection
- Réservation et rendu de jeux
- Profile
- Administration
- Ajoute/Suppresion de jeux
- Suppresion/Modification des utilisateurs

## Licence
Indiquez la licence sous laquelle le projet est distribué:
```
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
```
