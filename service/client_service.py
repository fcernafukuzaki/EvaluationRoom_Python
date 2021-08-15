from flask import jsonify
from configs.flask_config import db
from objects.client import Client, ClientSchema

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

class ClientService():

    def get_clients(self, idclient):
        if idclient:
            all_clients = Client.query.get((idclient))
        else:
            all_clients = Client.query.filter((Client.idcliente is not None)).order_by(Client.idcliente)
        
        if all_clients and idclient:
            result = client_schema.jsonify(all_clients)
            return result
        elif all_clients:
            result = clients_schema.dump(all_clients)
            return jsonify(result)
        return {'message': 'Not found'}, 404

    def add_client(self, idclient, nombre):
        new_client = Client(idclient, nombre)
        db.session.add(new_client)
        db.session.commit()
        return client_schema.jsonify(new_client)
    
    def update_client(self, idclient, nombre):
        client = Client.query.get((idclient))
        client.nombre = nombre

        db.session.commit()
        return client_schema.jsonify(client)

    def delete_client(self, idclient):
        client = Client.query.get((idclient))

        db.session.delete(client)
        db.session.commit()

        return client_schema.jsonify(client)