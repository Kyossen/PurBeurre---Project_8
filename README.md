# PurBeurre

PurBeurre est une plateforme web développée sous ## Django.
Le but principal de cette dernière est de permettre à un utilisateur de changer son alimentation.
En effet, la plateforme PurBeurre permet à un utilisateur d'entrée (dans un champs de recherche) un aliment (exepmle: Nutella),  et par la suite elle retournera à l'utilisateur une liste d'aliments avec un indice nutritionnel.
Bien évidemment, tout utilisateurs inscrits ou non peux accéder à cette recherche, ainsi qu'à une page déscription pour chaque aliment.



## A savoir :

Cette dernière fonctionne à l'aide d'une API externe:
### OpenFoodFact

Les indices nutrionnel varie entre "a" et "d" dans un ordre alphabétique.

Un utilisateur non inscrit ne pourra cependant pas accéder à un enregistrement de ces derniers.
Quant à l'utilisateur inscrit, lui aura accès à une section (favoris) ou il pourra sauvegarder s'il le souhaite des aliments afin de changer son alimentaiton.
La page description permet également d'accéder à la pge officiel de l'aliment OpenFoodFact via l'API, permettant d'avoir plus de détails en cas de nécessité.
