from fastapi import FastAPI, HTTPException
from recommender_chunk import RecommenderChunkSystem
from db_utils import get_movie, get_all_movies, get_movie_details, get_statistics, get_genre_distribution, get_ratings_chunk, get_ratings_user

app = FastAPI(title="API de recommendation de film")


ratings_df = None
recommender = None

if not ratings_df:
    print("Load system")
    ratings_df = get_ratings_chunk()
    print("Recommender system")
    recommender = RecommenderChunkSystem(ratings_df)
    print("End load system")



# Charger les données et entraîner le modèle au démarrage


@app.get("/movie/{movie_id}")
def get_movie_by_id(movie_id: int):
    try:
        movie = get_movie(movie_id)
        return movie
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Film introuvable")

@app.post("/recommendations/{user_id}")
def recommend_movies(user_id: int, top_n : int =10):

    all_movie_ids = get_all_movies()
    user_seen = get_ratings_user(user_id)['film_id'].to_list()

    unseen_movies = [m for m in all_movie_ids if m not in user_seen]

    if not unseen_movies:
        raise HTTPException(status_code=404, detail="Pas de recommandations disponibles")


    predictions = recommender.predict_for_user(user_id, unseen_movies)
    movie_ids = [pred['film_id'] for pred in predictions[:top_n]]
    movie_infos = get_movie_details(movie_ids)
    print(f" End predict movie for user {user_id}")
    # Joindre les prédictions avec les infos film
    response = []
    for movie in movie_infos:
        pred = next(p for p in predictions if p['film_id'] == movie['id'])
        movie['predicted_rating'] = pred['predicted_rating']
        response.append(movie)

    return response


@app.get("/statistics/{genre}/{year}")
def get_stats(genre: str | None, year: int | None):
    return get_statistics(genre, year)

@app.get("/genres/distribution")
def genre_distribution():
    return get_genre_distribution()

@app.get("/healthy")
def healthy():
    return "OK"
