import os
import duckdb

def export(database: str, export_dir: str = "/data/export"):
    """
    Exporte une base de données DuckDB dans un répertoire donné au format CSV.

    :param database: Chemin du fichier de la base de données DuckDB à exporter.
    :param export_dir: Chemin du répertoire où les fichiers exportés seront stockés.
    """
    # Création du répertoire d'exportation s'il n'existe pas
    if not os.path.exists(export_dir):
        os.makedirs(export_dir, exist_ok=True)

    # Connexion à la base de données et exécution de l'export
    con = duckdb.connect(database)
    con.execute(f"EXPORT DATABASE '{export_dir}' (FORMAT csv, DELIMITER ',');")
    con.close()
