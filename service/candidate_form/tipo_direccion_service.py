from flask import jsonify
from configs.resources import db
from objects.candidate_form.tipo_direccion import TipoDireccion, TipoDireccionSchema

tipos_direccion_schema = TipoDireccionSchema(many=True)

class TipoDireccionService():
    
    def get_tipos_direccion(self):
        all_tipos_direccion = TipoDireccion.query.all()
        if all_tipos_direccion:
            message = 'Se encontraron registros en base de datos.'
            return tipos_direccion_schema.dump(all_tipos_direccion), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message