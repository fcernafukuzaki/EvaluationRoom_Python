from flask import jsonify
from configs.flask_config import db
from objects.candidate import Candidate, CandidateDataSchema
from objects.candidate_telephone import CandidateTelephone
from objects.candidate_form.candidato_direccion import CandidatoDireccion
from objects.candidate_psychologicaltest import CandidatePsychologicalTest

candidate_data_schema = CandidateDataSchema()
candidates_data_schema = CandidateDataSchema(many=True)

class CandidateService():

    def get_candidate_by_uid(self, uid):
        try:
            if uid:
                candidato = Candidate.query.filter(Candidate.idcandidato==uid).first()
                print(candidato)
                if candidato:
                    result = candidate_data_schema.dump(candidato)
                    message = 'Existe candidato en base de datos.'
                    return result, 200, message
                message = f'No existe candidato en base de datos.'
                return None, 404, message
            return None, 400, 'Debe ingresar los parámetros.'
        except Exception as e:
            message = f'Hubo un error al obtener datos del candidato {uid} en base de datos {e}'
            return None, 503, message
    
    def get_candidate_by_email(self, correoelectronico):
        try:
            if correoelectronico:
                candidato = Candidate.query.filter(Candidate.correoelectronico==correoelectronico).first()
                print(candidato)
                if candidato:
                    result = candidate_data_schema.dump(candidato)
                    
                    message = 'Existe candidato en base de datos.'
                    return result, 200, message
                message = f'No existe candidato en base de datos.'
                return None, 404, message
        except Exception as e:
            message = f'Hubo un error al obtener datos del candidato {correoelectronico} en base de datos {e}'
            return None, 503, message

    def add_candidate(self, idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
                 cantidadhijos, fechanacimiento, correoelectronico, idsexo, selfregistration, telefonos, direcciones):
        try:
            new_candidate = Candidate(idcandidato, nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
                    cantidadhijos, fechanacimiento, correoelectronico, idsexo, selfregistration)
            db.session.add(new_candidate)
            db.session.commit()
            db.session.refresh(new_candidate)
            id_candidato = new_candidate.idcandidato

            if telefonos:
                self.delete_candidate_telephones(id_candidato)
                self.add_candidate_telephones(id_candidato, telefonos)
            
            if direcciones:
                self.delete_candidate_addresses(id_candidato)
                self.add_candidate_addresses(id_candidato, direcciones)
            
            message = 'Se registró candidato en base de datos.'
            return new_candidate.idcandidato, 200, message
        except Exception as e:
            message = f'Hubo un error al registrar candidato en base de datos {e}'
            return None, 503, message
    
    def add_candidate_tests(self, idcandidato, tests):
        try:
            for elemento_test in tests:
                new_candidate_psychologicaltest = CandidatePsychologicalTest(idcandidato, elemento_test['idTestPsicologico'])
                db.session.add(new_candidate_psychologicaltest)
                db.session.commit()
            
            message = f'Se registró pruebas psicológicas del candidato {idcandidato} en base de datos.'
            return True, 200, message
        except Exception as e:
            message = f'Hubo un error al registrar pruebas psicológicas del candidato {idcandidato} en base de datos {e}'
            return None, 503, message
    
    def update_candidate(self, idcandidate, nombre, apellidopaterno):
        selectionprocess = Candidate.query.get((idcandidate, nombre, apellidopaterno))
        selectionprocess.nombre = nombre
        selectionprocess.apellidopaterno = apellidopaterno

        db.session.commit()
        return candidate_data_schema.jsonify(selectionprocess)

    def add_candidate_telephones(self, idcandidate, telefonos):
        try:
            for elemento_telefono in telefonos:
                candidate_telephone = CandidateTelephone(idcandidate, elemento_telefono['idTelefono'], elemento_telefono['numero'])
                db.session.add(candidate_telephone)
                db.session.commit()
            message = 'Se registró datos de teléfono del candidato en base de datos.'
            return True, 200, message
        except Exception as e:
            message = f'Hubo un error al registrar datos de teléfono del candidato {idcandidate} en base de datos {e}'
            return None, 503, message
    
    def delete_candidate_telephones(self, idcandidate):
        try:
            candidate = CandidateTelephone.query.get((idcandidate))
            db.session.delete(candidate)
            db.session.commit()
            message = 'Se eliminó datos de teléfono del candidato en base de datos.'
            return True, 200, message
        except Exception as e:
            message = f'Hubo un error al eliminar datos de teléfono del candidato {idcandidate} en base de datos {e}'
            return None, 503, message
    
    def add_candidate_addresses(self, idcandidate, direcciones):
        try:
            for elemento_direccion in direcciones:
                idtipodireccion = elemento_direccion['idTipoDireccion']
                idpais = elemento_direccion['pais']['idPais']
                iddepartamento = elemento_direccion['departamento']['idDepartamento']
                idprovincia = elemento_direccion['provincia']['idProvincia']
                iddistrito = elemento_direccion['distrito']['idDistrito']
                direccion = elemento_direccion['direccion']
                
                candidato_direccion = CandidatoDireccion(idcandidate, idtipodireccion, idpais, iddepartamento, idprovincia, iddistrito, direccion)
                db.session.add(candidato_direccion)
                db.session.commit()
            message = 'Se registró datos de dirección del candidato en base de datos.'
            return True, 200, message
        except Exception as e:
            message = f'Hubo un error al registrar datos de dirección del candidato {idcandidate} en base de datos {e}'
            return None, 503, message
    
    def delete_candidate_addresses(self, idcandidate):
        try:
            candidate = CandidatoDireccion.query.get((idcandidate))
            db.session.delete(candidate)
            db.session.commit()
            message = 'Se eliminó datos de dirección del candidato en base de datos.'
            return True, 200, message
        except Exception as e:
            message = f'Hubo un error al eliminar datos de dirección del candidato {idcandidate} en base de datos {e}'
            return None, 503, message