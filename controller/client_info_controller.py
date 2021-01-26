from flask import request
from flask_restful import Resource
from dao.flask_config import app
from service.client_info_service import ClientInfoService

client_info_service = ClientInfoService()

class ClientInfoSimpleController(Resource):
    
    def get(self, idclient=None):
        return client_info_service.get_clients(idclient)
