from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
from configs.routes import api_add_resource

app = Flask(__name__)
api = Api(app)

CORS(app, resorces={r'/*': {"origins": '*'}})

# Importar la línea api.add_resource desde routes.py
api_add_resource(api)

if __name__ == '__main__':
    app.run()
