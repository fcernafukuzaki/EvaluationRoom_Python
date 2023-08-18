import pandas as pd
from configs.resources import db, text
from configs.logging import logger


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
            sql_query = f"""
            SELECT c.idcandidato, c.nombre, c.apellidopaterno, c.apellidomaterno, 
            c.fechanacimiento, c.correoelectronico, c.selfregistration, 
            c.iddocumentoidentidad, c.numerodocumentoidentidad, c.idestadocivil, 
            c.cantidadhijos, c.idsexo, c.fecharegistro,
            tel.idtelefono, tel.numero, 
            dir.idtipodireccion, dir.idpais, dir.iddepartamento, dir.idprovincia, dir.iddistrito, dir.direccion,
            test.idtestpsicologico
            FROM evaluationroom.candidato c
            LEFT JOIN evaluationroom.candidatotelefono tel ON c.idcandidato=tel.idcandidato
            LEFT JOIN evaluationroom.candidatodireccion dir ON c.idcandidato=dir.idcandidato
            LEFT JOIN evaluationroom.candidatotest test ON c.idcandidato=test.idcandidato
            WHERE c.idcandidato={uid}
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            
            if int(response_database.rowcount) > 0:
                # Obtén los resultados del cursor como una lista de diccionarios
                results = response_database.fetchall()

                # Convierte los resultados a un DataFrame de pandas
                df_results = pd.DataFrame(results)
                
                # Resultado en formato de lista
                obj_data = {
                    'idcandidato': None,
                    'nombre': None,
                    'apellidopaterno': None,
                    'apellidomaterno': None,
                    'fechanacimiento': None,
                    'correoelectronico': None,
                    'selfregistration': None,
                    'fecharegistro': None,
                    'iddocumentoidentidad': None,
                    'numerodocumentoidentidad': None,
                    'idestadocivil': None,
                    'cantidadhijos': None,
                    'idsexo': None
                }

                campos = ["idcandidato", "nombre", "apellidopaterno", "apellidomaterno", 
                "fechanacimiento", "correoelectronico", "selfregistration", "fecharegistro",
                "iddocumentoidentidad", "numerodocumentoidentidad", "idestadocivil", 
                "cantidadhijos", "idsexo"]
                df = df_results[campos].copy()
                unique_candidate = df[campos].drop_duplicates()
                unique_candidate["fechanacimiento"] = None if unique_candidate["fechanacimiento"][0] is None else unique_candidate["fechanacimiento"].dt.strftime('%Y-%m-%d').astype(str).replace("nan", None)
                unique_candidate["fecharegistro"] = unique_candidate["fecharegistro"].dt.strftime('%Y-%m-%d %H:%M:%S %Z').astype(str).replace("nan", None)
                unique_candidate = unique_candidate.to_dict(orient="records")

                campos = ["idcandidato", "idtelefono", "numero"]
                df = df_results[campos].copy()
                unique_telefonos = df[campos].drop_duplicates()
                unique_telefonos = unique_telefonos.to_dict(orient="records")

                campos = ["idcandidato", "idtipodireccion", "idpais", "iddepartamento", "idprovincia", "iddistrito", "direccion"]
                df = df_results[campos].copy()
                unique_direcciones = df[campos].drop_duplicates()
                unique_direcciones = unique_direcciones.to_dict(orient="records")

                campos = ["idcandidato", "idtestpsicologico"]
                df = df_results[campos].copy()
                unique_tests = df[campos].drop_duplicates()
                unique_tests = unique_tests.to_dict(orient="records")

                for row in unique_candidate:
                    obj_data['idcandidato'] = row.get("idcandidato")
                    obj_data['nombre'] = row.get("nombre")
                    obj_data['apellidopaterno'] = row.get("apellidopaterno")
                    obj_data['apellidomaterno'] = row.get("apellidomaterno")
                    obj_data['fechanacimiento'] = row.get("fechanacimiento")
                    obj_data['correoelectronico'] = row.get("correoelectronico")
                    obj_data['selfregistration'] = row.get("selfregistration")
                    obj_data['fecharegistro'] = row.get("fecharegistro")
                    obj_data['iddocumentoidentidad'] = row.get("iddocumentoidentidad")
                    obj_data['numerodocumentoidentidad'] = row.get("numerodocumentoidentidad")
                    obj_data['idestadocivil'] = row.get("idestadocivil")
                    obj_data['cantidadhijos'] = row.get("cantidadhijos")
                    obj_data['idsexo'] = row.get("idsexo")

                    obj_data['telephones'] = [
                        {
                            'idtelefono': row_telefono.get("idtelefono"),
                            'numero': row_telefono.get("numero")
                        }
                        for row_telefono in unique_telefonos
                        if row_telefono.get('idtelefono') is not None
                    ]
                    
                    obj_data['addresses'] = [
                        {
                            'idtipodireccion': row_direccion.get("idtipodireccion"),
                            'idpais': row_direccion.get("idpais"),
                            'iddepartamento': row_direccion.get("iddepartamento"),
                            'idprovincia': row_direccion.get("idprovincia"),
                            'iddistrito': row_direccion.get("iddistrito"),
                            'direccion': row_direccion.get("direccion")
                        }
                        for row_direccion in unique_direcciones
                        if row_direccion.get('idtipodireccion') is not None
                    ]
                    
                    obj_data['psychologicaltests'] = [
                        {
                            'idtestpsicologico': row_testpsicologico.get("idtestpsicologico")
                        }
                        for row_testpsicologico in unique_tests
                        if row_testpsicologico.get('idtestpsicologico') is not None
                    ]
                
                logger.debug("Response from candidato.", uid=uid)

                result, code, message = obj_data, 200, 'Se encontró candidato.'
            else:
                code, message = 404, 'No existe candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de los candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, message=message)
            return result, code, message

    
    # def get_candidate_by_email(self, correoelectronico):
    #     try:
    #         if correoelectronico:
    #             candidato = Candidate.query.filter(Candidate.correoelectronico==correoelectronico).first()
    #             print(candidato)
    #             if candidato:
    #                 result = candidate_data_schema.dump(candidato)
                    
    #                 message = 'Existe candidato en base de datos.'
    #                 return result, 200, message
    #             message = f'No existe candidato en base de datos.'
    #             return None, 404, message
    #     except Exception as e:
    #         message = f'Hubo un error al obtener datos del candidato {correoelectronico} en base de datos {e}'
    #         return None, 503, message


    # def get_candidate_by_document(self, numerodocumentoidentidad):
    #     try:
    #         if numerodocumentoidentidad:
    #             candidato = Candidate.query.filter(Candidate.numerodocumentoidentidad==numerodocumentoidentidad).first()
    #             print(candidato)
    #             if candidato:
    #                 result = candidate_data_schema.dump(candidato)
                    
    #                 message = 'Existe candidato en base de datos.'
    #                 return result, 200, message
    #             message = f'No existe candidato en base de datos.'
    #             return None, 404, message
    #     except Exception as e:
    #         message = f'Hubo un error al obtener datos del candidato {numerodocumentoidentidad} en base de datos {e}'
    #         return None, 503, message


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
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            uid, flag, message = self.__create_candidate(nombre, apellidopaterno, apellidomaterno, 
                                correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, 
                                idestadocivil, idsexo, cantidadhijos, fechanacimiento, 
                                selfregistration)
            if flag:
                self.__create_telephones(uid, telefonos)
                
                self.__create_addresses(uid, direcciones)
                
                self.__create_tests(uid, tests)
            
            result, code, message = uid, 201, 'Se registró candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar datos del candidato en base de datos {e}'
        finally:
            logger.info("Candidato inserted.", uid=uid, message=message)
            return result, code, message


    def __create_candidate(self, nombre:str, apellidopaterno:str, apellidomaterno:str, 
                            correoelectronico:str, iddocumentoidentidad:int, numerodocumentoidentidad:str, 
                            idestadocivil:int, idsexo:int, cantidadhijos:int, fechanacimiento:str, 
                            selfregistration:str):
        try:
            fechanacimiento = 'NULL' if fechanacimiento is None else f"'{fechanacimiento}'"
            
            sql_query = f"""
            INSERT INTO evaluationroom.candidato
            (nombre, apellidopaterno, apellidomaterno, iddocumentoidentidad, numerodocumentoidentidad, idestadocivil,
            cantidadhijos, fechanacimiento, correoelectronico, idsexo, selfregistration)
            VALUES 
            ('{nombre}', '{apellidopaterno}', '{apellidomaterno}', {iddocumentoidentidad}, '{numerodocumentoidentidad}', {idestadocivil},
            {cantidadhijos}, {fechanacimiento}, '{correoelectronico}', {idsexo}, '{selfregistration}')
            RETURNING idcandidato
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            new_candidate = db.execute(text(sql_query))
            db.commit()
            idcandidate = new_candidate.fetchone()[0]
            
            result, flag, message = idcandidate, True, 'Se registró datos del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = 0, False, f'Hubo un error al registrar datos del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato inserted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __update_data(self, idcandidate:int, nombre:str, apellidopaterno:str, apellidomaterno:str, 
               correoelectronico:str, iddocumentoidentidad:int, numerodocumentoidentidad:str, 
               idestadocivil:int, idsexo:int, cantidadhijos:int, fechanacimiento:str):
        try:
            sql_query = f"""
            UPDATE evaluationroom.candidato
            SET nombre='{nombre}', 
            apellidopaterno='{apellidopaterno}', 
            apellidomaterno='{apellidomaterno}', 
            correoelectronico='{correoelectronico}', 
            iddocumentoidentidad={iddocumentoidentidad}, 
            numerodocumentoidentidad='{numerodocumentoidentidad}', 
            idestadocivil={idestadocivil}, 
            idsexo={idsexo}, 
            cantidadhijos={cantidadhijos}, 
            fechanacimiento='{fechanacimiento}'
            WHERE idcandidato={idcandidate}
            """
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se actualizó candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al actualizar datos del candidato en base de datos {e}'
        finally:
            logger.info("Candidato updated.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __delete_data(self, idcandidate:int):
        try:
            sql_query = f"DELETE FROM evaluationroom.candidato WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó data del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar los datos del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato deleted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __delete_telephones(self, idcandidate:int):
        try:
            sql_query = f"DELETE FROM evaluationroom.candidatotelefono WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó teléfonos del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar los teléfonos del candidato en base de datos {e}'
        finally:
            logger.info("Teléfonos del candidato deleted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __create_telephones(self, idcandidate:int, telephones:list):
        try:
            for telephone in telephones:
                idtelefono = telephone.get("idtelefono")
                numero = telephone.get("numero")

                sql_query = f"""
                INSERT INTO evaluationroom.candidatotelefono
                (idtelefono, numero, idcandidato)
                VALUES 
                ({idtelefono}, '{numero}', {idcandidate})
                """
                
                # Ejecutar la consulta SQL y obtener los resultados en un dataframe
                response_database = db.execute(text(sql_query))
                db.commit()
                logger.debug("Teléfonos del candidato inserted.", idcandidate=idcandidate, idtelefono=idtelefono)
            
            result, flag, message = idcandidate, True, 'Se registró teléfonos del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al registrar teléfonos del candidato en base de datos {e}'
        finally:
            logger.info("Teléfonos del candidato inserted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __delete_addresses(self, idcandidate:int):
        try:
            sql_query = f"DELETE FROM evaluationroom.candidatodireccion WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó direcciones del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar las direcciones del candidato en base de datos {e}'
        finally:
            logger.info("Direcciones del candidato deleted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __create_addresses(self, idcandidate:int, addresses:list):
        try:
            for address in addresses:
                idtipodireccion = address.get("idtipodireccion")
                idpais = address.get("idpais")
                iddepartamento = address.get("iddepartamento")
                idprovincia = address.get("idprovincia")
                iddistrito = address.get("iddistrito")
                direccion = address.get("direccion")

                sql_query = f"""
                INSERT INTO evaluationroom.candidatodireccion
                (idtipodireccion, idpais, iddepartamento, idprovincia, iddistrito, direccion, idcandidato)
                VALUES 
                ({idtipodireccion}, {idpais}, {iddepartamento}, {idprovincia}, {iddistrito}, '{direccion}', {idcandidate})
                """
                
                # Ejecutar la consulta SQL y obtener los resultados en un dataframe
                response_database = db.execute(text(sql_query))
                db.commit()
                logger.debug("Direcciones del candidato inserted.", idcandidate=idcandidate, idtipodireccion=idtipodireccion)
            
            result, flag, message = idcandidate, True, 'Se registró direcciones del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al registrar direcciones del candidato en base de datos {e}'
        finally:
            logger.info("Direcciones del candidato inserted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __delete_tests(self, idcandidate:int):
        try:
            sql_query = f"DELETE FROM evaluationroom.candidatotest WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó tests del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar los tests del candidato en base de datos {e}'
        finally:
            logger.info("Tests del candidato deleted.", idcandidate=idcandidate, message=message)
            return result, flag, message


    def __create_tests(self, idcandidate:int, tests:list):
        try:
            for test in tests:
                idtestpsicologico = test.get("idtestpsicologico")

                sql_query = f"""
                INSERT INTO evaluationroom.candidatotest
                (idtestpsicologico, idcandidato)
                VALUES 
                ({idtestpsicologico}, {idcandidate})
                """
                
                # Ejecutar la consulta SQL y obtener los resultados en un dataframe
                response_database = db.execute(text(sql_query))
                db.commit()
                logger.debug("Tests del candidato inserted.", idcandidate=idcandidate, idtestpsicologico=idtestpsicologico)
            
            result, flag, message = idcandidate, True, 'Se registró tests del candidato.'
        except Exception as e:
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al registrar tests del candidato en base de datos {e}'
        finally:
            logger.info("Tests del candidato inserted.", idcandidate=idcandidate, message=message)
            return result, flag, message

    
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
            result, flag, message = self.__update_data(uid, nombre, apellidopaterno, apellidomaterno, 
                                                       correoelectronico, iddocumentoidentidad, numerodocumentoidentidad, 
                                                       idestadocivil, idsexo, cantidadhijos, fechanacimiento)
            
            if flag:
                _, flag_telephones, message = self.__delete_telephones(uid)
                self.__create_telephones(uid, telefonos) if flag_telephones is True else _, flag_telephones, message
                
                _, flag_addresses, message = self.__delete_addresses(uid)
                self.__create_addresses(uid, direcciones) if flag_addresses is True else _, flag_addresses, message
                
                _, flag_tests, message = self.__delete_tests(uid)
                self.__create_tests(uid, tests) if flag_tests is True else _, flag_tests, message
            
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
            _, flag_telephones, message = self.__delete_telephones(uid)
            _, flag_addresses, message = self.__delete_addresses(uid)
            _, flag_tests, message = self.__delete_tests(uid)
            _, flag, message = self.__delete_data(uid)
                
            result, code, message = uid, 204, 'Se eliminó candidato.'
        except Exception as e:
            code, message = 503, f'Hubo un error al eliminar datos de los candidato en base de datos {e}'
        finally:
            logger.info("Candidato deleted.", uid=uid, message=message)
            return result, code, message
