from flask import request
from flask_restful import Resource
from dao.flask_config import app
from service.client_service import ClientService

client_service = ClientService()

class ClientController(Resource):
    
    def get(self, idclient=None):
        return client_service.get_clients(idclient)

    def post(self):
        nombre = request.json['nombre']
        
        new_client = client_service.add_client(None, nombre)
        
        return new_client

    def put(self):
        idclient = request.json['idclient']
        nombre = request.json['nombre']

        return client_service.update_client(idclient, nombre)

    def delete(self):
        idclient = request.json['idclient']
        
        return client_service.delete_client(idclient)