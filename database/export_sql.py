import os

import duckdb

def export(database : str):
    dir_export = "/data/export"
    if ( not os.path.exists(dir_export)):
        os.mkdir(dir_export)

    con = duckdb.connect(database)
    con.sql(f"EXPORT DATABASE '{dir_export}' (FORMAT csv, DELIMITER ',');")
    con.close
