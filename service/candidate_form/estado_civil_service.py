from flask import jsonify
from configs.resources import db
from objects.candidate_form.estado_civil import EstadoCivil, EstadoCivilSchema

estados_civil_schema = EstadoCivilSchema(many=True)

class EstadoCivilService():
    
    def get_estados_civil(self):
        all_estados_civil = EstadoCivil.query.all()
        if all_estados_civil:
            message = 'Se encontraron registros en base de datos.'
            return estados_civil_schema.dump(all_estados_civil), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message