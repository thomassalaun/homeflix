import pandas as pd
import ast
import os
from duckdb import connect
from sqlalchemy import create_engine, table, column
from sqlalchemy.dialects.postgresql import insert
from schema import create_tables
from export_sql import export


def insert_do_nothing_on_conflicts(sqltable, conn, keys, data_iter):
    columns=[]
    for c in keys:
        columns.append(column(c))

    if sqltable.schema:
        table_name = '{}.{}'.format(sqltable.schema, sqltable.name)
    else:
        table_name = sqltable.name

    mytable = table(table_name, *columns)
    data = [dict(zip(keys, row)) for row in data_iter]
    for rr in data:
        data_eval = ast.literal_eval(str(rr['genres']))

        # Extraire les IDs
        ids = [str(obj['id']) for obj in data_eval]
        rr['genres'] = ' '.join(ids)
    insert_stmt = insert(mytable).values(data)
    do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['id'])

    conn.execute(do_nothing_stmt)

def create_database(db_path : str):
    con = connect(db_path)
    con.close()

def load_data(db_path: str):
   # Créer une instance DuckDB
    engine = create_engine(f"duckdb://{db_path}")
    conn = engine.connect()

    # Création des tables
    create_tables(engine)

    # Charger les données depuis Kaggle
    df_ratings = pd.read_csv('/data/ratings_small.csv')
    df_movies = pd.read_csv('/data/movies_metadata.csv', usecols=['id', 'title','genres','overview','release_date','vote_average','vote_count'])
    ##, converters={"genres": lambda x: json.loads(x.replace("'", '"'))}

    df_ratings = df_ratings.rename(columns={'movieId': 'film_id','userId' : 'user_id'})
    df_movies = df_movies.rename(columns={'overview':'description'})
    # Insérer les données dans DuckDB
    print("Chargement des films.")
    df_movies.to_sql('films', con=conn,if_exists='append', chunksize=5000, index=False, method=insert_do_nothing_on_conflicts)
    print("Chargement des évaluations.")
    df_ratings.to_sql('ratings', con=conn, if_exists='replace', index=False,chunksize=2000, method='multi')

    print("📥 Données chargées avec succès.")

if __name__ == '__main__':
    db_path = os.getenv("PATH_DATA") + "/ma_base.duckdb"
    create_database(db_path)
    load_data(db_path)
    export(db_path)
