import pandas as pd
import json
import duckdb

def nettoyer_et_importer_csv(input_path, db_path, table_name):
    """
    Nettoie un fichier CSV et importe les données dans une table DuckDB.

    :param input_path: str, Chemin du fichier CSV d'entrée.
    :param db_path: str, Chemin de la base de données DuckDB.
    :param table_name: str, Nom de la table DuckDB.
    """
    try:
        # Charger le fichier CSV
        df = pd.read_csv(input_path)

        # Nettoyer les colonnes JSON
        colonnes_json = [
            'genres', 
            'belongs_to_collection', 
            'production_companies', 
            'production_countries', 
            'spoken_languages'
        ]
        for col in colonnes_json:
            if col in df.columns:
                df[col] = df[col].fillna('[]').apply(
                    lambda x: json.dumps(eval(x)) if isinstance(x, str) and (x.startswith('[') or x.startswith('{')) else '{}'
                )

        # Convertir les colonnes de types spécifiques
        if 'adult' in df.columns:
            df['adult'] = df['adult'].astype(bool)
        if 'video' in df.columns:
            df['video'] = df['video'].astype(bool)
        if 'release_date' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.date

        # Se connecter à DuckDB
        conn = duckdb.connect(db_path)
        try:
            # Supprimer la table existante si nécessaire
            conn.execute(f"DROP TABLE IF EXISTS {table_name}")

            # Enregistrer et créer la table
            conn.register("temp_df", df)
            conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
            print(f"Table '{table_name}' créée avec succès dans la base de données '{db_path}'.")

            # Afficher quelques lignes pour validation
            print("Aperçu des données :")
            print(conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf())
        finally:
            conn.close()
    except FileNotFoundError:
        print(f"Fichier introuvable : {input_path}")
    except pd.errors.ParserError as e:
        print(f"Erreur de parsing CSV : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    # Définir les chemins et nom de la table
    input_csv = "data/movies_kaggle.csv"
    db_path = "data/movies.db"
    table_name = "movies_kaggle"
    
    nettoyer_et_importer_csv(input_csv, db_path, table_name)
