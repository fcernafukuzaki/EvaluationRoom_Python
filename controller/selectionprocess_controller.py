from flask import request
from flask_restful import Resource
from configs.resources import app
from service.authorizer_service import AuthorizerService
from dashboard.selectionprocess_service import SelectionProcessService
from service.login_user_service import LoginUserService

authorizer_service = AuthorizerService()
selectionprocess_service = SelectionProcessService()
login_user_service = LoginUserService()

class SelectionProcessController(Resource):
    
    def get(self, idclient=None, idjobposition=None, process_status=None):
        token = request.headers['Authorization']
        validate = authorizer_service.validate_hash(token)
        if validate:
            return selectionprocess_service.get_selectionprocesses(idclient, idjobposition, process_status)
        return {'message': 'User not registered'}, 403

    def post(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        date_process_begin = request.json['date_process_begin']
        date_process_end = request.json['date_process_end']
        user_register = request.json['user_register']
        process_active = request.json['process_active']
        
        new_selectionprocess = selectionprocess_service.add_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)
        
        return new_selectionprocess

    def put(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']
        date_process_begin = request.json['date_process_begin']
        date_process_end = request.json['date_process_end']
        user_register = request.json['user_register']
        process_active = request.json['process_active']

        return selectionprocess_service.update_selectionprocess(idclient, idjobposition, date_process_begin, date_process_end, user_register, process_active)

    def delete(self):
        idclient = request.json['idclient']
        idjobposition = request.json['idjobposition']

        return selectionprocess_service.delete_selectionprocess(idclient, idjobposition)