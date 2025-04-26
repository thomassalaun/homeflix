import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('duckdb:///data/ma_base.duckdb?access_mode=read_only')

def get_ratings_chunk(user_id=None):
    where_clause = ""
    if user_id:
        where_clause = f"user_id = {user_id}"
    query = f"""
    SELECT user_id, film_id, rating 
    FROM ratings
    {f"WHERE {where_clause}" if where_clause else ""}
    """
    return pd.read_sql(query, engine,chunksize=40000)

def get_ratings_user(user_id=None):
    where_clause = ""
    if user_id:
        where_clause = f"user_id = {user_id}"
    query = f"""
    SELECT user_id, film_id, rating 
    FROM ratings
    {f"WHERE {where_clause}" if where_clause else ""}
    """
    return pd.read_sql(query, engine)

def get_ratings(user_id=None):
    where_clause = ""
    if user_id:
        where_clause = f"user_id = {user_id}"
    query = f"""
    SELECT user_id, film_id, rating 
    FROM ratings
    {f"WHERE {where_clause}" if where_clause else ""}
    """
    return pd.read_sql(query, engine)

def get_movie(movie_id: int):
    query = f"SELECT id, title, genres, description, release_date, vote_average, vote_count FROM films WHERE id = {movie_id}"
    return pd.read_sql(query, engine).to_dict(orient='records')[0]

def get_all_movies():
    query = "SELECT id FROM films"
    return pd.read_sql(query, engine)['id'].tolist()

def get_movie_details(movie_ids: list[int]):
    ids_str = ','.join(map(str, movie_ids))
    query = f"SELECT * FROM films WHERE id IN ({ids_str})"
    return pd.read_sql(query, engine).to_dict(orient='records')

def get_statistics(genre=None, year=None):
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
    query = "SELECT genres FROM films"
    df = pd.read_sql(query, engine)

    # Compter les genres
    from collections import Counter
    genre_counter = Counter()

    for genres in df['genres']:
        if pd.notna(genres):
            for g in genres.split(' '):
                genre_counter[g.strip()] += 1

    genre_df = pd.DataFrame(genre_counter.items(), columns=["genre", "count"])
    genre_df = genre_df.sort_values(by="count", ascending=False)
    return genre_df.to_dict(orient='records')
