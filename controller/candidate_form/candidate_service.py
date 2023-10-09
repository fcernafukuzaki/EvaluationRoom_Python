from configs.logging import logger
from repository.candidate_repository import CandidateRepository


candidaterepository = CandidateRepository()


class CandidateService():

    def get_by_uid(self, uid:int):
        """ 
        Descripción:
            Obtener datos del candidato.
        Input:
            - uid:int Identificador del candidato.
        Output:
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            flag, message, obj_data = candidaterepository.get_by_uid(uid=uid)
            if flag:
                result, code, message = obj_data, 200, 'Se encontró candidato.'
            else:
                code, message = 404, 'No existe candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, message=message)
            return result, code, message

    
    def get_by_email(self, correoelectronico):
        """ 
        Descripción:
            Obtener datos del candidato por correo electrónico.
        Input:
            - correoelectronico:string Correo electrónico del candidato.
        Output:
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            uid = None
            if correoelectronico:
                flag, message, uid = candidaterepository.get_by_email(correoelectronico=correoelectronico)
                
                if flag:
                    flag, message, result = candidaterepository.get_by_uid(uid=uid)
                    code = 200 if flag else 404
                else:
                    code, message = 404, f'No existe candidato con el correo electrónico {correoelectronico}.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos del candidato {correoelectronico} en base de datos {e}'
        finally:
            logger.info("Candidato by email.", uid=uid, message=message)
            return result, code, message


    def get_by_document(self, numerodocumentoidentidad):
        """ 
        Descripción:
            Obtener datos del candidato por número de documento de identidad.
        Input:
            - numerodocumentoidentidad:string Número de documento de identidad.
        Output:
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            uid = None
            if numerodocumentoidentidad:
                flag, message, uid = candidaterepository.get_by_document(numerodocumentoidentidad=numerodocumentoidentidad)
                
                if flag:
                    flag, message, result = candidaterepository.get_by_uid(uid=uid)
                    code = 200 if flag else 404
                else:
                    code, message = 404, f'No existe candidato con el número de documento de identidad {numerodocumentoidentidad}.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos del candidato {numerodocumentoidentidad} en base de datos {e}'
        finally:
            logger.info("Candidato by document.", uid=uid, message=message)
            return result, code, message


    def create(self, nombre:str, apellidopaterno:str, apellidomaterno:str, 
                correoelectronico:str, iddocumentoidentidad:int, numerodocumentoidentidad:str, 
                idestadocivil:int, idsexo:int, cantidadhijos:int, fechanacimiento:str, 
                selfregistration:str, telefonos:list, direcciones:list, tests:list):
        """ 
        Descripción:
            Registrar datos de un candidato.
        Input:
            - nombre:string Nombre del candidato.
            - apellidopaterno:string Apellido paterno del candidato.
            - apellidomaterno:string Apellido materno del candidato.
            - correoelectronico:string Correo electrónico del candidato.
            - iddocumentoidentidad:int Identificador del documento de identidad.
            - numerodocumentoidentidad:string Número de documento de identidad.
            - idestadocivil:int Identificador de estado civil.
            - idsexo:int Identificador del sexo del candidato.
            - cantidadhijos:int Cantidad de hijos que tiene el candidato.
            - fechanacimiento:date Fecha de nacimiento en formato YYYY-MM-DD. 
            - selfregistration:bool Indicador si el candidato fue registrado (False) o se registró por si mismo (True).
            - telefonos: Lista de teléfonos del candidato (celular y/o teléfono fijo).
            - direcciones: Lista de direcciones del candidato (domicilio y/o lugar de nacimiento).
            - tests: Lista de test psicológicos asignados al candidato.
        Output:
            - data: Identificador del candidato.
        """
        result = None
        try:
            flag, message, uid = candidaterepository.insert(nombre, apellidopaterno, apellidomaterno, 
                                                            correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, 
                                                            idestadocivil, idsexo, cantidadhijos, fechanacimiento, selfregistration)
            if flag:
                candidaterepository.insert_telephones(uid, telefonos)
                candidaterepository.insert_addresses(uid, direcciones)
                candidaterepository.insert_tests(uid, tests)
            
            result, code, message = uid, 201, 'Se registró candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar datos del candidato en base de datos {e}'
        finally:
            logger.info("Candidato inserted.", uid=uid, message=message)
            return result, code, message

    
    def update(self, uid:int, nombre:str, apellidopaterno:str, apellidomaterno:str, 
               correoelectronico:str, iddocumentoidentidad:int, numerodocumentoidentidad:str, 
               idestadocivil:int, idsexo:int, cantidadhijos:int, fechanacimiento:str, 
               telefonos:list, direcciones:list, tests:list):
        """ 
        Descripción:
            Actualizar datos de un candidato.
        Input:
            - uid:int Identificador del candidato.
            - nombre:string Nombre del candidato.
            - apellidopaterno:string Apellido paterno del candidato.
            - apellidomaterno:string Apellido materno del candidato.
            - correoelectronico:string Correo electrónico del candidato.
            - iddocumentoidentidad:int Identificador del documento de identidad.
            - numerodocumentoidentidad:string Número de documento de identidad.
            - idestadocivil:int Identificador de estado civil.
            - idsexo:int Identificador del sexo del candidato.
            - cantidadhijos:int Cantidad de hijos que tiene el candidato.
            - fechanacimiento:date Fecha de nacimiento en formato YYYY-MM-DD. 
            - telefonos: Lista de teléfonos del candidato (celular y/o teléfono fijo).
            - direcciones: Lista de direcciones del candidato (domicilio y/o lugar de nacimiento).
            - tests: Lista de test psicológicos asignados al candidato.
        Output:
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            flag, message, result = candidaterepository.update(uid, nombre, apellidopaterno, apellidomaterno, 
                                                               correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, 
                                                               idestadocivil, idsexo, cantidadhijos, fechanacimiento)
            
            if flag:
                flag_telephones, message, _ = candidaterepository.delete_telephones(uid)
                candidaterepository.insert_telephones(uid, telefonos) if flag_telephones else _, flag_telephones, message
                
                flag_addresses, message, _ = candidaterepository.delete_addresses(uid)
                candidaterepository.insert_addresses(uid, direcciones) if flag_addresses else _, flag_addresses, message
                
                flag_tests, message, _ = candidaterepository.delete_tests(uid)
                candidaterepository.insert_tests(uid, tests) if flag_tests else _, flag_tests, message
            
            result, code, message = uid, 200, 'Se actualizó candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar datos de los candidato en base de datos {e}'
        finally:
            logger.info("Candidato updated.", uid=uid, message=message)
            return result, code, message


    def delete(self, uid:int):
        """ 
        Descripción:
            Actualizar datos de un candidato.
        Input:
            - uid:int Identificador del candidato.
        Output:
            - None
        """
        result = None
        try:
            candidaterepository.delete_telephones(uid)
            candidaterepository.delete_addresses(uid)
            candidaterepository.delete_tests(uid)
            candidaterepository.delete(uid)
                
            result, code, message = uid, 204, 'Se eliminó candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar datos de los candidato en base de datos {e}'
        finally:
            logger.info("Candidato deleted.", uid=uid, message=message)
            return result, code, message


    def json_candidate(self, input_json):
        nombre, apellidopaterno, apellidomaterno = input_json.get('nombre'), input_json.get('apellidoPaterno'), input_json.get('apellidoMaterno')
        correoelectronico = str(input_json.get('correoElectronico', '')).lower()
        iddocumentoidentidad = input_json.get('documentoIdentidad')['idDocumentoIdentidad'] if input_json.get('documentoIdentidad') is not None else 1
        numerodocumentoidentidad = input_json.get('numeroDocumentoIdentidad', '')
        idestadocivil = input_json.get('estadoCivil')['idEstadoCivil'] if input_json.get('estadoCivil') is not None else 1
        idsexo = input_json.get('sexo')['idSexo'] if input_json.get('sexo') is not None else 1
        cantidadhijos = input_json.get('cantidadHijos', 0)
        fechanacimiento = input_json.get('fechaNacimiento')
        
        telefonos = [
            {
                'idtelefono': row.get("idTelefono"),
                'numero': row.get("numero")
            }
            for row in input_json.get('telefonos')
            if row.get('idTelefono') is not None
        ]

        direcciones = [
            {
                'idtipodireccion': row.get("idTipoDireccion"),
                'idpais': row.get("pais")["idPais"] if row.get("pais") is not None else None,
                'iddepartamento': row.get("departamento")["idDepartamento"] if row.get("departamento") is not None else None,
                'idprovincia': row.get("provincia")["idProvincia"] if row.get("provincia") is not None else None,
                'iddistrito': row.get("distrito")["idDistrito"] if row.get("distrito") is not None else None,
                'direccion': row.get("direccion")
            }
            for row in input_json.get('direcciones')
            if row.get('idTipoDireccion') is not None
        ]

        tests = [
            {
                'idtestpsicologico': row.get("idTestPsicologico")
            }
            for row in input_json.get('testPsicologicos')
            if row.get('idTestPsicologico') is not None
        ]
        return nombre, apellidopaterno, apellidomaterno, correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil, idsexo, cantidadhijos, fechanacimiento, telefonos, direcciones, tests