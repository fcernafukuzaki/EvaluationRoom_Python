from flask import jsonify
from configs.flask_config import db
from objects.candidate_form.distrito import Distrito, DistritoSchema

distritos_schema = DistritoSchema(many=True)

class DistritoService():
    
    def get_distritos_by_ids(self, id_country, id_departamento, id_provincia):
        all_distritos = Distrito.query.filter(Distrito.idpais==id_country, 
                                              Distrito.iddepartamento==id_departamento,
                                              Distrito.idprovincia==id_provincia).all()
        if all_distritos:
            message = 'Se encontraron registros en base de datos.'
            return distritos_schema.dump(all_distritos), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message