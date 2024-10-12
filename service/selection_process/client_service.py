from flask import jsonify
from configs.resources import db
from objects.selection_process.client import Client, ClientSchema
from objects.selection_process.client_info import ClientInfo, ClientInfoSchema

client_schema = ClientSchema()
clients_info_schema = ClientInfoSchema(many=True)

class ClientService():

    def get_clients(self):
        result, code, message = None, 404, 'No existe cliente.'
        try:
            clients = db.session.query(Client).order_by(Client.idcliente)

            if clients.count():
                result, code, message = clients_info_schema.dump(clients), 200, 'Se encontró clientes.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de clientes en base de datos {e}'
        finally:
            print(message)
            return result, code, message

    def get_client(self, uid):
        result, code, message = None, 404, 'No existe cliente.'
        try:
            client = db.session.query(Client).filter(Client.idcliente==uid).order_by(Client.idcliente).all()
            
            if client:
                result, code, message = client_schema.dump(client[0]), 200, 'Se encontró cliente.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos del cliente {uid} en base de datos {e}'
        finally:
            print(message)
            return result, code, message

    def add_client(self, nombre):
        result = None
        try:
            new_client = Client(None, nombre)
            db.session.add(new_client)
            db.session.commit()
            db.session.refresh(new_client)
            result = new_client.idcliente
            code, message = 200, 'Se registró cliente en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar cliente en base de datos {e}'
        finally:
            print(message)
            return result, code, message
    
    def update_client(self, uid, nombre):
        result = None
        try:
            client = Client.query.get((uid))
            client.nombre = nombre
            db.session.commit()
            result, code, message = uid, 200, 'Se actualizó cliente en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar cliente en base de datos {e}'
        finally:
            print(message)
            return result, code, message

    def delete_client(self, uid):
        result = None
        try:
            client = Client.query.get((uid))
            db.session.delete(client)
            db.session.commit()
            result, code, message = uid, 200, 'Se eliminó cliente en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar cliente en base de datos {e}'
        finally:
            print(message)
            return result, code, message