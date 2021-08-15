from flask import jsonify
from configs.flask_config import db
from objects.client_info import ClientInfo, ClientInfoSchema

clients_info_schema = ClientInfoSchema(many=True)

class ClientInfoService():

    def get_clients(self, idclient):        
        if idclient:
            all_clients = Client.query.filter(Client.idcliente==idclient).all()
        else:
            all_clients = ClientInfo.all_clients_resumen
        
        if all_clients:
            result = clients_info_schema.dump(all_clients)
            return jsonify(result)
        return {'message': 'Not found'}, 404
