import pandas as pd
from sqlalchemy import create_engine
from collections import Counter

# Configuration de la base de données
engine = create_engine('duckdb:///data/ma_base.duckdb?access_mode=read_only')

def get_ratings_chunk(user_id=None, chunk_size=40000):
    """
    Récupère les évaluations en morceaux depuis la table `ratings`.

    :param user_id: int, Filtrer par ID utilisateur (optionnel).
    :param chunk_size: int, Taille des morceaux de données (par défaut 40 000).
    :return: Generator[pd.DataFrame], morceaux de données.
    """
    where_clause = f"WHERE user_id = {user_id}" if user_id else ""
    query = f"SELECT user_id, film_id, rating FROM ratings {where_clause}"
    return pd.read_sql(query, engine, chunksize=chunk_size)

def get_ratings(user_id=None):
    """
    Récupère toutes les évaluations ou celles d'un utilisateur spécifique.

    :param user_id: int, Filtrer par ID utilisateur (optionnel).
    :return: pd.DataFrame, données des évaluations.
    """
    where_clause = f"WHERE user_id = {user_id}" if user_id else ""
    query = f"SELECT user_id, film_id, rating FROM ratings {where_clause}"
    return pd.read_sql(query, engine)

def get_movie(movie_id):
    """
    Récupère les détails d'un film par son ID.

    :param movie_id: int, ID du film.
    :return: dict, détails du film.
    """
    query = f"""
    SELECT id, title, genres, description, release_date, vote_average, vote_count
    FROM films WHERE id = {movie_id}
    """
    return pd.read_sql(query, engine).to_dict(orient='records')[0]

def get_all_movies():
    """
    Récupère les IDs de tous les films.

    :return: list[int], liste des IDs de films.
    """
    query = "SELECT id FROM films"
    return pd.read_sql(query, engine)['id'].tolist()

def get_movie_details(movie_ids):
    """
    Récupère les détails d'une liste de films par leurs IDs.

    :param movie_ids: list[int], liste des IDs de films.
    :return: list[dict], liste des détails des films.
    """
    ids_str = ','.join(map(str, movie_ids))
    query = f"SELECT * FROM films WHERE id IN ({ids_str})"
    return pd.read_sql(query, engine).to_dict(orient='records')

def get_statistics(genre=None, year=None):
    """
    Calcule les statistiques sur les films en fonction des genres et de l'année.

    :param genre: str, Filtrer par genre (optionnel).
    :param year: str, Filtrer par année (optionnel).
    :return: list[dict], statistiques agrégées.
    """
    conditions = []
    if genre:
        conditions.append(f"genres LIKE '%{genre}%'")
    if year:
        conditions.append(f"SUBSTR(release_date, 1, 4) = '{year}'")

    where_clause = " AND ".join(conditions)
    query = f"""
    SELECT f.id, f.title, f.genres, f.release_date,
           AVG(r.rating) AS average_rating,
           COUNT(r.rating) AS num_ratings
    FROM films f
    JOIN ratings r ON f.id = r.film_id
    {f"WHERE {where_clause}" if where_clause else ""}
    GROUP BY f.id, f.title, f.genres, f.release_date
    ORDER BY average_rating DESC
    """
    return pd.read_sql(query, engine).to_dict(orient='records')

def get_genre_distribution():
    """
    Calcule la distribution des genres dans les films.

    :return: list[dict], distribution des genres.
    """
    query = "SELECT genres FROM films"
    df = pd.read_sql(query, engine)

    # Compter les genres
    genre_counter = Counter()
    for genres in df['genres'].dropna():
        for genre in genres.split():
            genre_counter[genre.strip()] += 1

    genre_df = pd.DataFrame(genre_counter.items(), columns=["genre", "count"])
    genre_df = genre_df.sort_values(by="count", ascending=False)
    return genre_df.to_dict(orient='records')
