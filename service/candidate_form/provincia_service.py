from flask import jsonify
from configs.flask_config import db
from objects.candidate_form.provincia import Provincia, ProvinciaSchema

provincias_schema = ProvinciaSchema(many=True)

class ProvinciaService():
    
    def get_provincias_by_ids(self, id_country, id_departamento):
        all_provincias = Provincia.query.filter(Provincia.idpais==id_country, 
                                                Provincia.iddepartamento==id_departamento).all()
        if all_provincias:
            message = 'Se encontraron registros en base de datos.'
            return provincias_schema.dump(all_provincias), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message