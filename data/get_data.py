import requests
import pandas as pd

API_KEY = input("Votre clé API TMDB: ")  # Ma clé : e05037d502da3d12dda1283bf62e9da8
URL = "https://api.themoviedb.org/3/movie/popular"
PARAMS = {"api_key": API_KEY, "language": "en-EN"}

def fetch_popular_movies(api_url, params, total_pages=10):
    all_movies = []
    for page in range(1, total_pages + 1):
        params["page"] = page
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data['results'])
            print(f"Page {page} récupérée.")
        else:
            print(f"Erreur {response.status_code} à la page {page} : {response.text}")
            break
    return all_movies

# Spécifie combien de pages tu veux récupérer
total_pages = input('Combien de pages à récupérer ? ')
movies = fetch_popular_movies(URL, PARAMS, total_pages=int(total_pages))
df_movies = pd.DataFrame(movies)

print(df_movies.columns)

# Garde uniquement les colonnes qui t'intéressent
df_movies = df_movies[['id', 'title', 'overview', 'release_date', 'vote_average', 'vote_count', 'genre_ids']]

# Affiche un aperçu des données
print(df_movies.head())

# Sauvegarde en CSV
df_movies.to_csv("data/movies_popular.csv", index=False)
print("Données sauvegardées dans 'data/movies_popular.csv'")
