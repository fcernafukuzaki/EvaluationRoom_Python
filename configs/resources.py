from os import environ
from sqlalchemy import create_engine, text


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        host = environ.get("HOST")
        database = environ.get("DATABASE")
        user = environ.get("USER")
        password = environ.get("PASSWORD")
        engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{database}')

        conn = engine.connect()
        print("Connected")
        
        return conn
    except Exception as error:
        print(error)
        

db = connect()
