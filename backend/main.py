from fastapi import FastAPI, HTTPException
from recommender_chunk import RecommenderChunkSystem
from db_utils import get_movie, get_all_movies, get_movie_details, get_statistics, get_genre_distribution, get_ratings_chunk, get_ratings

app = FastAPI(title="API de Recommandation de Films")

# Variables globales pour les données et le système de recommandation
ratings_df = None
recommender = None

if not ratings_df :
    ratings_df = get_ratings_chunk()
    print("Initialisation du système de recommandation...")
    recommender = RecommenderChunkSystem(ratings_df)
    print("Système chargé avec succès.")

@app.get("/movie/{movie_id}")
def get_movie_by_id(movie_id: int):
    """
    Récupère les informations d'un film par son ID.

    :param movie_id: ID du film.
    :return: Détails du film.
    """
    try:
        movie = get_movie(movie_id)
        return movie
    except Exception as e:
        print(f"Erreur : {e}")
        raise HTTPException(status_code=404, detail="Film introuvable.")

@app.post("/recommendations/{user_id}")
def recommend_movies(user_id: int, top_n: int = 10):
    """
    Recommande des films à un utilisateur.

    :param user_id: ID de l'utilisateur.
    :param top_n: Nombre maximum de recommandations à renvoyer.
    :return: Liste des recommandations avec les détails des films et les notes prédites.
    """
    try:
        all_movie_ids = get_all_movies()
        user_seen = get_ratings(user_id)['film_id'].tolist()
        unseen_movies = [m for m in all_movie_ids if m not in user_seen]

        if not unseen_movies:
            raise HTTPException(status_code=404, detail="Pas de recommandations disponibles.")

        predictions = recommender.predict_for_user(user_id, unseen_movies)
        top_predictions = predictions[:top_n]
        movie_ids = [pred['film_id'] for pred in top_predictions]
        movie_infos = get_movie_details(movie_ids)

        response = [
            {**movie, "predicted_rating": next(p['predicted_rating'] for p in top_predictions if p['film_id'] == movie['id'])}
            for movie in movie_infos
        ]
        return response
    except Exception as e:
        print(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération des recommandations.")

@app.get("/statistics/{genre}/{year}")
def get_stats(genre: str | None = None, year: int | None = None):
    """
    Récupère les statistiques des films en fonction d'un genre et/ou d'une année.

    :param genre: Genre à filtrer (optionnel).
    :param year: Année à filtrer (optionnel).
    :return: Statistiques des films.
    """
    try:
        return get_statistics(genre, year)
    except Exception as e:
        print(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des statistiques.")

@app.get("/genres/distribution")
def genre_distribution():
    """
    Récupère la distribution des genres dans les films.

    :return: Distribution des genres.
    """
    try:
        return get_genre_distribution()
    except Exception as e:
        print(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération de la distribution des genres.")

@app.get("/healthy")
def healthy():
    """
    Vérifie la santé du service.

    :return: Message de confirmation.
    """
    return "OK"
