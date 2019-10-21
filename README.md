# PurBeurre
PurBeurre est une plateforme web développée sous Django.  

## Fonctionnement:
Le but principal de cette dernière, est de permettre à un utilisateur de changer son alimentation.  
En effet, la plateforme PurBeurre permet à un utilisateur d'entrée (dans un champs de recherche) un aliment, par exemple: Nutella  
Par la suite, elle affichera une liste de produits en fonction de ce dernier avec un indice nutritionnel.  
Bien évidemment, tout utilisateurs inscrits ou non, peut accéder à cette recherche, ainsi qu'à une page déscription pour chaque aliment.  
La plateforme PurBeurre fonctionne à l'aide de l'API externe suivante:
#### OpenFoodFact

## A savoir :
- Les indices nutrionnels varie entre "a" et "d" dans un ordre alphabétique.
- Un utilisateur non inscrit ne pourra pas accéder à un enregistrement d'aliment en favoris.
- La page description permet également d'accéder à la page officiel de l'aliment OpenFoodFact via son API, permettant d'avoir plus de détails en cas de nécessité.
- Ce repos est pré-alablement configuré pour une mise en développement.
- Ce repos est pré-alablement configuré à l'utilisation de test avec "TestCase" et "Selenium". Il dispose également de "Coverage"

## Pré-requis:
- Python 3.x
- Django
- PostgreSQL
- HTML5
- CSS3 & BootStrap
- JavaScript & JQuery
- GeckoDriver (Pour Selenium sous Windows)

## Utilisation:

### Première étape:
- Installer les pré-requis

### Seconde étape:
- Installer "requirements.txt" -> pip install -r requirements.txt

### Troisième étape:
#### Configurer les variables d'environnement
- Ouvrer le fichier "settings.py" afin d'accéder à ces variables (exemple: os.environ.get('DB_PORT'))  
PS: Set -> Windows & Export -> Linux

### Quatrième étape:
#### Sous Windows
- python3 manage.py init_db.py
- python3 manage.py runserver
#### Sous Linux
- ./manage.py init_db.py ou python3 manage.py init_db.py runserver
- ./manage.py runserver ou python3 manage.py runserver

### Dernière étape:
- Connecter vous à l'adresse local affichée.
