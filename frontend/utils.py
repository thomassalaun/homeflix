import requests
import pandas as pd

API_URL = "http://homeflix-backend:8000"

def get_recommendations(user_id: int, top_n: int = 5):
    url = f"{API_URL}/recommendations/{user_id}?top_n={top_n}"
    res = requests.post(url)
    return res.json() if res.status_code == 200 else []

def get_movie(movie_id: int):
    url = f"{API_URL}/movie/{movie_id}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else {}

def get_user_rated_movies(user_id: int):
    # ici on lit directement dans DuckDB dans la version finale,
    # mais pour l'instant on simule ça par une API future ou un appel local
    # Ex: ajouter plus tard un endpoint `/user/{id}/rated`
    return []

def fetch_genre_distribution():
    res = requests.get(f"{API_URL}/genres/distribution")
    return res.json() if res.status_code == 200 else []

def fetch_stats(genre=None, year=None):
    res = requests.get(f"{API_URL}/statistics/{genre}/{year}")
    return res.json() if res.status_code == 200 else []