# PurBeurre
PurBeurre est une plateforme web développée sous Django.  

## Fonctionnement:
Le but principal de cette dernière est de permettre à un utilisateur de changer son alimentation.  
En effet, la plateforme PurBeurre permet à un utilisateur d'entrée (dans un champs de recherche) un aliment (exepmle: Nutella),  et par la suite elle retournera à l'utilisateur une liste d'aliments avec un indice nutritionnel.  
Bien évidemment, tout utilisateurs inscrits ou non peux accéder à cette recherche, ainsi qu'à une page déscription pour chaque aliment.  
Cette dernière fonctionne à l'aide d'une API externe:
#### OpenFoodFact

## A savoir :
- Les indices nutrionnels varie entre "a" et "d" dans un ordre alphabétique.
- Un utilisateur non inscrit ne pourra pas accéder à un enregistrement d'aliment en favoris.
- Un utilisateur inscrit aura accès à l'enregistrement.
- La page description permet également d'accéder à la page officiel de l'aliment OpenFoodFact via son API, permettant d'avoir plus de détails en cas de nécessité.

## Pré-requis:
- Python 3.x
- Django
- PostgreSQL
- HTML5
- CSS3 & BootStrap
- JavaScript & JQuery

## Utilisation:

### Première étape:
- Installer les pré-requis

### Seconde étape:
- Installer le fichier "requirements.txt" -> pip install -r requirements.txt

### Troisème étape:
#### Sous Windows
python3 manage.py runserver
#### Sous Linux
./manage.py runserver ou python3 manage.py runserver
