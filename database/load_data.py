import os
import ast
import pandas as pd
import ast
from duckdb import connect
from sqlalchemy import create_engine, table, column
from sqlalchemy.dialects.postgresql import insert
from schema import create_tables
from export_sql import export


def insert_do_nothing_on_conflicts(sqltable, conn, keys, data_iter):
    """
    Insère des données dans une table en ignorant les conflits.

    :param sqltable: Table SQLAlchemy.
    :param conn: Connexion SQLAlchemy.
    :param keys: Liste des clés/colonnes.
    :param data_iter: Itérateur sur les données à insérer.
    """
    # Créer une liste de colonnes SQLAlchemy
    columns = [column(c) for c in keys]

    # Définir le nom complet de la table
    table_name = f"{sqltable.schema}.{sqltable.name}" if sqltable.schema else sqltable.name
    mytable = table(table_name, *columns)

    # Préparer les données à insérer
    data = [dict(zip(keys, row)) for row in data_iter]
    for row in data:
        genres_data = ast.literal_eval(str(row['genres']))
        # Extraire les IDs de genres et les convertir en chaîne
        ids = [str(obj['id']) for obj in genres_data]
        row['genres'] = ' '.join(ids)

    # Construire et exécuter la requête d'insertion
    insert_stmt = insert(mytable).values(data)
    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['id'])
    conn.execute(do_nothing_stmt)


def create_database(db_path: str):
    """
    Crée une base de données DuckDB vide.

    :param db_path: Chemin de la base de données.
    """
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    con = connect(db_path)
    con.close()
    print(f"Base de données créée à {db_path}")


def load_data(db_path: str):
    """
    Charge les données dans la base de données DuckDB.

    :param db_path: Chemin de la base de données.
    """
    # Créer une instance SQLAlchemy pour DuckDB
    engine = create_engine(f"duckdb://{db_path}")
    conn = engine.connect()

    # Créer les tables nécessaires
    create_tables(engine)

    # Charger les données depuis les fichiers CSV
    df_ratings = pd.read_csv('/data/ratings_small.csv')
    df_movies = pd.read_csv(
        '/data/movies_metadata.csv',
        usecols=['id', 'title', 'genres', 'overview', 'release_date', 'vote_average', 'vote_count']
    )

    # Renommer les colonnes pour correspondre à la base
    df_ratings = df_ratings.rename(columns={'movieId': 'film_id', 'userId': 'user_id'})
    df_movies = df_movies.rename(columns={'overview': 'description'})

    # Insérer les données dans DuckDB
    print("🔄 Chargement des films...")
    df_movies.to_sql('films', con=conn, if_exists='append', chunksize=5000, index=False, method=insert_do_nothing_on_conflicts)
    print("🔄 Chargement des évaluations...")
    df_ratings.to_sql('ratings', con=conn, if_exists='replace', index=False, chunksize=2000, method='multi')

    print("📥 Données chargées avec succès.")


if __name__ == '__main__':
    # Chemin de la base de données
    db_path = "/data/ma_base.duckdb"
    
    # Créer la base de données, charger les données, et exporter
    create_database(db_path)
    load_data(db_path)
    export(db_path)
