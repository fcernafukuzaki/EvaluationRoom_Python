from flask import jsonify
from configs.resources import db
from objects.candidate_form.documento_identidad import DocumentoIdentidad, DocumentoIdentidadSchema

documentos_identidad_schema = DocumentoIdentidadSchema(many=True)

class DocumentoIdentidadService():
    
    def get_documentos_identidad(self):
        all_documentos_identidad = DocumentoIdentidad.query.all()
        if all_documentos_identidad:
            message = 'Se encontraron registros en base de datos.'
            return documentos_identidad_schema.dump(all_documentos_identidad), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message