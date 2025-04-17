import duckdb
import pandas as pd

# Chemins vers les fichiers et noms des tables
movies_tmdb_file = "data/movies_tmdb.csv"
movies_tmdb_table_name = "movies_tmdb"

movies_kaggle_file = "data/movies_kaggle.csv"
movies_kaggle_table_name = "movies_kaggle"

ratings_file = "data/ratings_kaggle.csv"  
ratings_table_name = "ratings"

# Créer une base DuckDB (fichier .db)
db_connection = duckdb.connect("movies.db")

# Charger les données des films de TMDB dans une table

def charge_csv(path_file, name_table, types=None):
    try:
        # Créer la table à partir du fichier CSV avec des options pour contourner les erreurs
        if types is None : 
            db_connection.execute(f"""
                CREATE TABLE {name_table} AS 
                SELECT * FROM read_csv_auto(
                    '{path_file}', 
                    strict_mode=false  -- Ignore les erreurs strictes
                )
            """)
        
        print(f"Table '{name_table}' créée avec succès.")
        # Vérifier la structure et un aperçu de la table
        print("Colonnes dans la table :")
        print(db_connection.execute(f"DESCRIBE {name_table}").fetchall())
        print("Quelques lignes :")
        print(db_connection.execute(f"SELECT * FROM {name_table} LIMIT 5").fetchdf())

    except Exception as e:
        print(f"Aucune table '{name_table}' créée. Erreur :", e)

# Le CSV movies_kaggle contient des données JSON que DuckDB ne comprend pas
def clean_csv(input_path, output_path):
    try:
        # Lire le fichier
        df = pd.read_csv(input_path)

        # Colonnes à normaliser (JSON)
        colonnes_json = ['genres', 'belongs_to_collection', 'production_companies', 'production_countries']

        for col in colonnes_json:
            if col in df.columns:
                df[col] = df[col].fillna('[]')  # Remplacer NaN par des listes vides
                df[col] = df[col].apply(eval)  # Convertir la chaîne JSON en liste/dict

        # Sauvegarder un nouveau fichier CSV
        df.to_csv(output_path, index=False)
        print(f"Fichier nettoyé sauvegardé sous : {output_path}")
    except Exception as e:
        print("Erreur lors du nettoyage :", e)

# Charger les CSV
#charge_csv(movies_tmdb_file, movies_tmdb_table_name)
types_kaggle = {"belongs_to_collection": "JSON",
                "genres": "JSON",
                "spoken_languages": "JSON",
                "production_countries": "JSON",
                "production_companies": "JSON"}
#charge_csv(movies_kaggle_file, movies_kaggle_table_name, types_kaggle)
#charge_csv(ratings_file, ratings_table_name)

#clean_csv(movies_kaggle_file, 'test.csv')
charge_csv('data/movies_kaggle.csv', 'test')
# Fermer la connexion
db_connection.close()
