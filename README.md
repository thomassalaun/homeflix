# MESSAGE IMPORTANT

Le fichier CONSIGNES.md contient les consignes du prof telles que l'on les a reçues. Je note aussi le lien de son repo pour avoir le projet à l'état zéro : https://github.com/Elias-Hr/homeflix

## IL FAUT TELECHARGER L'ARCHIVE DE DATA SUR https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/ 
On garde les fichiers 'ratings.csv' et 'movies_metadata' qu'il faut glisser dans le dossier 'data'.

# Ce que j'ai fait :

- Récupérer les données :
   - Kaggle : sur le lien, https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset/, j'utilise 'ratings.csv' (renommé en 'data/ratings_kaggle') et 'movies_metadata' (renommé en 'data/movies_kaggle')
   - quelques données des films les plus populaires du moment avec l'api de TMDB : programme get_data.py

- Clean le dataset 'data/movies_kaggle' pour que DuckDB le comprenne : programme json_clean.py

# Ce que j'ai partiellement fait :

- Mettre les trois tables dans un fichier .db
   - IMPORTANT : voir le fichier HELPME.md qui contient des instructions du prof à ce sujet

# Ce qu'il faut faire : 

- Faire une structure propre pour que tous les fichiers utilisés pour la data (.csv, .py, .db) soient au même endroit

- Est-ce que ça du sens d'avoir plein de fichiers python comme ça ? Est-ce que un script global est pas mieux ? Mais alors comment s'y retrouver ? Est-ce que c'est possible de faire exécuter des fichiers python dans un ordre pour "créer" l'application une fois le projet fini ?

- Merge les deux datasets de film (juste crée le programme merge_movies.py)
   - la clé de jointure étant l'id du film 
   - attention, beaucoup d'infos du dataset de Kaggle sont superflues et n'existe pas dans celui de TMDB, donc il faut **supprimer les colonnes superflues**