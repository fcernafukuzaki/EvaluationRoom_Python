from flask import Flask
from flask_restful import Api
from configs.routes import api_add_resource

app = Flask(__name__)
api = Api(app)

# Importar la línea api.add_resource desde routes.py
api_add_resource(api)

if __name__ == '__main__':
    app.run()
