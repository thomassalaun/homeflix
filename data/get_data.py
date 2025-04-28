import requests
import pandas as pd

def fetch_popular_movies(api_url, params, total_pages=10):
    """
    Récupère les films populaires depuis l'API TMDB.

    Args:
        api_url (str): URL de l'API TMDB.
        params (dict): Paramètres de la requête API.
        total_pages (int): Nombre total de pages à récupérer.

    Returns:
        list: Liste des films populaires.
    """
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

if __name__ == "__main__":
    # Entrée de l'utilisateur pour la clé API et le nombre de pages
    API_KEY = input("Votre clé API TMDB: ")
    URL = "https://api.themoviedb.org/3/movie/popular"
    PARAMS = {"api_key": API_KEY, "language": "en-EN"}
    
    try:
        total_pages = int(input("Combien de pages à récupérer ? "))
    except ValueError:
        print("Veuillez entrer un nombre entier valide.")
        exit(1)

    # Récupération des données
    movies = fetch_popular_movies(URL, PARAMS, total_pages=total_pages)
    if not movies:
        print("Aucune donnée récupérée. Fin du script.")
        exit(1)
    
    # Transformation des données en DataFrame
    df_movies = pd.DataFrame(movies)
    print(df_movies.columns)
    
    # Filtrage des colonnes pertinentes
    columns_to_keep = ['id', 'title', 'overview', 'release_date', 'vote_average', 'vote_count', 'genre_ids']
    if all(column in df_movies.columns for column in columns_to_keep):
        df_movies = df_movies[columns_to_keep]
    else:
        print("Certaines colonnes nécessaires manquent dans les données récupérées.")
        exit(1)
    
    # Affichage d'un aperçu des données
    print(df_movies.head())
    
    # Sauvegarde des données en fichier CSV
    output_path = "data/csv/movies_popular.csv"
    try:
        df_movies.to_csv(output_path, index=False)
        print(f"Données sauvegardées dans '{output_path}'")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du fichier CSV : {e}")
