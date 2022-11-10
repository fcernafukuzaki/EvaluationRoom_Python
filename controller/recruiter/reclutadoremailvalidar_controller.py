from flask import request
from flask_restful import Resource
from configs.flask_config import app
from service.recruiter.reclutadoridentificadorvalidar_service import ReclutadorIdentificadorValidarService
from objects.usuario import Usuario, UsuarioSchema

reclutadoridentificadorvalidar_service = ReclutadorIdentificadorValidarService()
usuario_schema = UsuarioSchema()


class ReclutadorEmailValidarController(Resource):

    def post(self):
        token = request.json['Authorization']
        email_reclutador = request.json['correoelectronico']

        email_valido, mensaje, usuario = reclutadoridentificadorvalidar_service.valida_email_reclutador(email_reclutador)
        if email_valido:
            return usuario_schema.jsonify(usuario)
        return {'mensaje': mensaje}, 404