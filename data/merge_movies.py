import duckdb

db_connection = duckdb.connect("movies.db")

# Vérifier les colonnes de la table 'movies'
print("Colonnes de 'movies_tmdb':")
print(db_connection.execute("DESCRIBE movies_tmdb").fetchdf())

# Vérifier les colonnes de la table 'movies_metadata'
print("Colonnes de 'movies_kaggle':")
print(db_connection.execute("DESCRIBE movies_kaggle").fetchdf())
