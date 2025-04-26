from sqlalchemy import MetaData, Table, Column, Integer, String, Float

metadata = MetaData()

movies = Table(
    'films', metadata,
    Column('id', Integer,autoincrement=False, primary_key=True),
    Column('title', String),
    Column('genres', String),
    Column('description', String),
    Column('release_date', String),
    Column('vote_average', Float),
    Column('vote_count', Integer)
)


ratings = Table(
    'ratings', metadata,
    Column('user_id', Integer),
    Column('film_id', Integer),
    Column('rating', Float),
    Column('timestamp', Integer)
)

def create_tables(engine):
    metadata.create_all(engine)
