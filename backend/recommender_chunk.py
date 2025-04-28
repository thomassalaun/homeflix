from collections.abc import Iterator
from surprise import SVD, Dataset, Reader
import pandas as pd

class RecommenderChunkSystem:
    """
    Système de recommandation basé sur le modèle SVD de Surprise.
    Permet de construire un modèle à partir de données de notes en chunks.

    Attributes:
        model (SVD): Modèle SVD entraîné sur l'ensemble des données.
    """

    def __init__(self, ratings_df: Iterator[pd.DataFrame]):
        """
        Initialise le système de recommandation et entraîne le modèle.

        :param ratings_df: Un itérateur de DataFrame contenant les colonnes ['user_id', 'film_id', 'rating'].
        """
        # Liste pour accumuler les chunks et définir les bornes des notes
        data_chunks = []
        min_rating, max_rating = float('inf'), float('-inf')

        # Prétraitement des données chunk par chunk
        for chunk in ratings_df:
            # Sélection des colonnes pertinentes
            chunk = chunk[['user_id', 'film_id', 'rating']]
            min_rating = min(min_rating, chunk['rating'].min())
            max_rating = max(max_rating, chunk['rating'].max())
            data_chunks.append(chunk)

        # Combinaison de tous les chunks en un DataFrame unique
        full_df = pd.concat(data_chunks)

        # Configuration du lecteur Surprise avec l'échelle des notes
        reader = Reader(rating_scale=(min_rating, max_rating))

        # Chargement des données dans le format Surprise
        data = Dataset.load_from_df(full_df, reader)

        # Construction du trainset et entraînement du modèle SVD
        trainset = data.build_full_trainset()
        self.model = SVD()
        self.model.fit(trainset)

    def predict_for_user(self, user_id: int, movie_ids: list[int]) -> list[dict]:
        """
        Prédit les notes pour un utilisateur donné sur une liste de films.

        :param user_id: ID de l'utilisateur pour lequel générer des prédictions.
        :param movie_ids: Liste des IDs des films pour lesquels prédire les notes.
        :return: Liste triée des prédictions avec les IDs des films et les notes prédites.
        """
        predictions = [
            {
                'film_id': movie_id,
                'predicted_rating': round(self.model.predict(user_id, movie_id).est, 2)
            }
            for movie_id in movie_ids
        ]
        return sorted(predictions, key=lambda x: x['predicted_rating'], reverse=True)
