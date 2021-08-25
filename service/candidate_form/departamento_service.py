from flask import jsonify
from configs.flask_config import db
from objects.candidate_form.departamento import Departamento, DepartamentoSchema

departamentos_schema = DepartamentoSchema(many=True)

class DepartamentoService():
    
    def get_departamentos_by_country(self, id_country):
        all_departamentos = Departamento.query.filter(Departamento.idpais==id_country).all()
        if all_departamentos:
            message = 'Se encontraron registros en base de datos.'
            return departamentos_schema.dump(all_departamentos), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message