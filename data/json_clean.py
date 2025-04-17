import pandas as pd
import json
import duckdb

def nettoyer_et_importer_csv(input_path, db_path, table_name):
    """
    Nettoie un fichier CSV et importe les données dans une table DuckDB.

    :param input_path: Chemin du fichier CSV d'entrée.
    :param db_path: Chemin de la base de données DuckDB.
    :param table_name: Nom de la table DuckDB.
    """
    # Charger le fichier CSV
    df = pd.read_csv(input_path)

    # Colonnes JSON à nettoyer
    colonnes_json = ['genres', 'belongs_to_collection', 'production_companies', 'production_countries', 'spoken_languages']
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

    # Se connecter à DuckDB et importer les données
    conn = duckdb.connect(db_path)
    try:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.register("temp_df", df)
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
        print(f"Table '{table_name}' créée avec succès dans la base de données {db_path}.")
        print("Quelques lignes :")
        print(conn.execute(f"SELECT * FROM {table_name} LIMIT 5").fetchdf())
    except Exception as e:
        print("Erreur lors de la création de la table :", e)
    finally:
        conn.close()

# Utilisation
input_csv = "data/movies_kaggle.csv"
db_path = "data/movies.db"
table_name = "movies_kaggle"
nettoyer_et_importer_csv(input_csv, db_path, table_name)
