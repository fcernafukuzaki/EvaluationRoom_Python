from os import environ
from sqlalchemy import create_engine, text


# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from flask_restful import Api
# from flask_cors import CORS, cross_origin


# DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
# DATABASE_URI = DATABASE_URI[1 : len(DATABASE_URI) - 1]

# # Aplicación de servidor
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# api = Api(app)

# CORS(app)

# # with app.app_context():
# #     db = SQLAlchemy(app)
# #     ma = Marshmallow(app)
# #     api = Api(app)


#!/usr/bin/python
# from configparser import ConfigParser


# def config(filename='database.ini', section='postgresql'):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)

#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))

#     return db


def connect():
    """ Connect to the PostgreSQL database server """
    # conn = None
    try:
        # read connection parameters
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        host = environ.get("HOST")
        database = environ.get("DATABASE")
        user = environ.get("USER")
        password = environ.get("PASSWORD")
        engine = create_engine(f'postgresql://{user}:{password}@{host}:5432/{database}')

        conn = engine.connect()
        print("Connected")
        # conn = psycopg2.connect(
        #         host=environ.get("HOST"),
        #         database=environ.get("DATABASE"),
        #         user=environ.get("USER"),
        #         password=environ.get("PASSWORD"))
		
        # create a cursor
        # cur = conn.cursor()
        
	# execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')

        # # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        # cur.close()

        return conn
    except Exception as error:
        print(error)
        # conn.close()
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')


db = connect()
