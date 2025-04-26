from collections.abc import Iterator

from surprise import SVD, Dataset, Reader
import pandas as pd

class RecommenderChunkSystem:
    def __init__(self, ratings_df:  Iterator[pd.DataFrame]):
        data_chunks = []
        min = 2000
        max = -2000

        for chunk in ratings_df:
            chunk = chunk[['user_id', 'film_id', 'rating']]
            min_tmp = chunk['rating'].min()
            max_tmp = chunk['rating'].max()
            min = min if min < min_tmp else min_tmp
            max = max if max > max_tmp else max_tmp
            data_chunks.append(chunk)


        full_df = pd.concat(data_chunks)
        reader = Reader(rating_scale=(min, max))
        data = Dataset.load_from_df(full_df, reader)
        trainset = data.build_full_trainset()
        self.model = SVD()
        self.model.fit(trainset)


    def predict_for_user(self, user_id: int, movie_ids: list[int]) -> list[dict]:
        predictions = []
        for movie_id in movie_ids:
            pred = self.model.predict(user_id, movie_id)
            predictions.append({
                'film_id': movie_id,
                'predicted_rating': round(pred.est, 2)
            })
        return sorted(predictions, key=lambda x: x['predicted_rating'], reverse=True)
