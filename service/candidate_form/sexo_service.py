from flask import jsonify
from configs.flask_config import db
from objects.candidate_form.sexo import Sexo, SexoSchema

sexos_schema = SexoSchema(many=True)

class SexoService():
    
    def get_sexos(self):
        all_sexos = Sexo.query.all()
        if all_sexos:
            message = 'Se encontraron registros en base de datos.'
            return sexos_schema.dump(all_sexos), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message