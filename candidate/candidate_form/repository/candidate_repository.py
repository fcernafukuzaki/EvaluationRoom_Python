import pandas as pd
from configs.resources import db, text
from configs.logging import logger


class CandidateRepository():
    
    def get_by_uid(self, uid:int):
        """ 
        Descripción:
            Obtener datos del candidato a partir de un identificador.
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
            
            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))
            
            if int(response_database.rowcount) > 0:
                # Resultados del cursor como una lista de diccionarios y convertir a un DataFrame
                result = response_database.fetchall()
                df_results = pd.DataFrame(result)
                
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
                    obj_data = {
                        'idcandidato': row.get("idcandidato"),
                        'nombre': row.get("nombre"),
                        'apellidopaterno': row.get("apellidopaterno"),
                        'apellidomaterno': row.get("apellidomaterno"),
                        'fechanacimiento': row.get("fechanacimiento"),
                        'correoelectronico': row.get("correoelectronico"),
                        'selfregistration': row.get("selfregistration"),
                        'fecharegistro': row.get("fecharegistro"),
                        'iddocumentoidentidad': row.get("iddocumentoidentidad"),
                        'numerodocumentoidentidad': row.get("numerodocumentoidentidad"),
                        'idestadocivil': row.get("idestadocivil"),
                        'cantidadhijos': row.get("cantidadhijos"),
                        'idsexo': row.get("idsexo")
                    }

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
                
                # logger.debug("Response from candidato.", uid=uid)

                result, flag, message = obj_data, True, 'Se encontró candidato.'
            else:
                flag, message = False, 'No existe candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener datos de los candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, message=message)
            return flag, message, result


    def get_by_email(self, correoelectronico:str):
        """ 
        Descripción:
            Obtener identificador del candidato a partir de su correo electrónico.
        Input:
            - correoelectronico:string Correo electrónico del candidato.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
        result = None
        uid = None
        try:
            sql_query = f"""
            SELECT c.idcandidato
            FROM evaluationroom.candidato c
            WHERE c.correoelectronico='{correoelectronico}'
            ORDER BY c.idcandidato
            """

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))
            
            if int(response_database.rowcount) > 0:
                uid = response_database.fetchone().idcandidato
                result, flag, message = uid, True, 'Se encontró candidato.'
            else:
                flag, message = False, 'No existe candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener uid del candidato en base de datos {e}'
        finally:
            # logger.info("Response from candidato.", uid=uid, correoelectronico=correoelectronico, message=message)
            return flag, message, result


    def get_by_document(self, numerodocumentoidentidad:str):
        """ 
        Descripción:
            Obtener identificador del candidato a partir de su número de documento de identidad.
        Input:
            - numerodocumentoidentidad:string Número de documento de identidad.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
        result = None
        uid = None
        try:
            sql_query = f"""
            SELECT c.idcandidato
            FROM evaluationroom.candidato c
            WHERE c.numerodocumentoidentidad='{numerodocumentoidentidad}'
            ORDER BY c.idcandidato
            """

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))
            
            if int(response_database.rowcount) > 0:
                uid = response_database.fetchone().idcandidato
                result, flag, message = uid, True, 'Se encontró candidato.'
            else:
                flag, message = False, 'No existe candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener uid del candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, numerodocumentoidentidad=numerodocumentoidentidad, message=message)
            return flag, message, result


    def insert(self, nombre:str, apellidopaterno:str, apellidomaterno:str, correoelectronico:str, iddocumentoidentidad:int, numerodocumentoidentidad:str, 
               idestadocivil:int, idsexo:int, cantidadhijos:int, fechanacimiento:str, selfregistration:str):
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
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
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
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = 0, False, f'Hubo un error al registrar datos del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato inserted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def insert_telephones(self, idcandidate:int, telephones:list):
        """ 
        Descripción:
            Registrar teléfonos de un candidato.
        Input:
            - idcandidate:int Identificador del candidato.
            - telephones:list Lista de teléfonos del candidato (celular y/o teléfono fijo).
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
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
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al registrar teléfonos del candidato en base de datos {e}'
        finally:
            logger.info("Teléfonos del candidato inserted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def insert_addresses(self, idcandidate:int, addresses:list):
        """ 
        Descripción:
            Registrar teléfonos de un candidato.
        Input:
            - idcandidate:int Identificador del candidato.
            - addresses:list Lista de direcciones del candidato (domicilio y/o lugar de nacimiento).
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
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
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al registrar direcciones del candidato en base de datos {e}'
        finally:
            logger.info("Direcciones del candidato inserted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def insert_tests(self, idcandidate:int, tests:list):
        """ 
        Descripción:
            Registrar test psicológicos a un candidato.
        Input:
            - idcandidate:int Identificador del candidato.
            - tests:list Lista de test psicológicos asignados al candidato.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
        try:
            for idtestpsicologico in tests:
                sql_query = '''INSERT INTO evaluationroom.candidatotest \
                (idtestpsicologico, idcandidato) \
                VALUES \
                (:idtestpsicologico, :idcandidate) \
                '''
                
                data = {'idcandidate': idcandidate, 'idtestpsicologico': idtestpsicologico}
                
                # Ejecutar la consulta SQL y obtener los resultados en un dataframe
                response_database = db.execute(text(sql_query), data)
                db.commit()
                logger.debug("Tests del candidato inserted.", idcandidate=idcandidate, idtestpsicologico=idtestpsicologico)
            
            result, flag, message = idcandidate, True, 'Se registró tests del candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al registrar tests del candidato en base de datos {e}'
        finally:
            logger.info("Tests del candidato inserted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def get_tests_id(self, idcandidate:int):
        """ 
        Descripción:
            Obtener los identificadores de los test psicológicos de un candidato.
        Input:
            - idcandidate:int Identificador del candidato.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Lista de identificador de los tests psicológicos asignados al candidato.
        """
        result = None
        try:
            sql_query = '''SELECT idtestpsicologico \
                FROM evaluationroom.candidatotest \
                WHERE idcandidato = :idcandidato \
            '''
            data = {'idcandidato': idcandidate}
            response_database = db.execute(text(sql_query), data)
            
            if int(response_database.rowcount) > 0:
                result = [
                    test.idtestpsicologico 
                    for test in response_database
                ]
                flag, message = True, 'Se encontró tests del candidato.'
            else:
                flag, message = False, 'No candidato no tiene tests asignados.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al obtener los tests del candidato en base de datos {e}'
        finally:
            return flag, message, result


    def update(self, idcandidate:int, nombre:str, apellidopaterno:str, apellidomaterno:str, 
               correoelectronico:str, iddocumentoidentidad:int, numerodocumentoidentidad:str, 
               idestadocivil:int, idsexo:int, cantidadhijos:int, fechanacimiento:str):
        """ 
        Descripción:
            Actualizar datos de un candidato.
        Input:
            - idcandidate:int Identificador del candidato.
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
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
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
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al actualizar datos del candidato en base de datos {e}'
        finally:
            logger.info("Candidato updated.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def delete(self, idcandidate:int):
        """ 
        Descripción:
            Eliminar un candidato a partir de su identificador.
        Input:
            - idcandidate:int Identificador del candidato.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - result: Identificador del candidato.
        """
        try:
            sql_query = f"DELETE FROM evaluationroom.candidato WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó data del candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar los datos del candidato en base de datos {e}'
        finally:
            logger.info("Datos del candidato deleted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def delete_telephones(self, idcandidate:int):
        try:
            sql_query = f"DELETE FROM evaluationroom.candidatotelefono WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó teléfonos del candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar los teléfonos del candidato en base de datos {e}'
        finally:
            logger.info("Teléfonos del candidato deleted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def delete_addresses(self, idcandidate:int):
        try:
            sql_query = f"DELETE FROM evaluationroom.candidatodireccion WHERE idcandidato={idcandidate}"
            
            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            response_database = db.execute(text(sql_query))
            db.commit()
            
            result, flag, message = idcandidate, True, 'Se eliminó direcciones del candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar las direcciones del candidato en base de datos {e}'
        finally:
            logger.info("Direcciones del candidato deleted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def delete_tests(self, idcandidate:int, tests:list):
        try:
            for idtest in tests:
                sql_query = '''DELETE FROM evaluationroom.candidatotest \
                    WHERE idcandidato = :idcandidato \
                    AND idtestpsicologico = :idtestpsicologico
                '''
                data = {'idcandidato': idcandidate, 'idtestpsicologico': idtest}
                response_database = db.execute(text(sql_query), data)
                db.commit()
                logger.info("Test del candidato deleted.", idcandidate=idcandidate, ids_test=idtest)
            
            result, flag, message = idcandidate, True, 'Se eliminó tests del candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            result, flag, message = idcandidate, False, f'Hubo un error al eliminar los tests del candidato en base de datos {e}'
        finally:
            logger.info("Tests del candidato deleted.", idcandidate=idcandidate, message=message)
            return flag, message, result


    def get_evaluation_by_uid(self, uid:int):
        """ 
        Descripción:
            Obtener datos del candidato para iniciar su evaluación.
        Input:
            - uid:int Identificador del candidato.
        Output:
            - data: Objeto de datos del candidato.
        """
        result = None
        try:
            sql_query = f"""
            SELECT c.idcandidato, c.nombre, c.apellidopaterno, c.apellidomaterno, 
            c.nombre || ' ' || c.apellidopaterno || ' ' || c.apellidomaterno AS "nombre_completo",
            c.fechanacimiento, c.correoelectronico, c.selfregistration, 
            (SELECT COUNT(ctest.idcandidato) 
                FROM evaluationroom.candidatotest ctest
                WHERE ctest.idcandidato=c.idcandidato) AS "cantidad_pruebas_asignadas",
            (SELECT COUNT(ctest.idcandidato) 
                FROM evaluationroom.candidatotest ctest
                WHERE ctest.idcandidato=c.idcandidato
                AND ctest.fechaexamen IS NULL) AS "cantidad_pruebas_pendientes"
            FROM evaluationroom.candidato c
            WHERE c.idcandidato={uid}
            """

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))
            
            if int(response_database.rowcount) > 0:
                # Resultados del cursor como una lista de diccionarios y convertir a un DataFrame
                result = response_database.fetchall()
                df_results = pd.DataFrame(result)

                # Resultado en formato de lista
                obj_data = {
                    'idcandidato': None,
                    'nombre': None,
                    'apellidopaterno': None,
                    'apellidomaterno': None,
                    'nombre_completo': None,
                    'fechanacimiento': None,
                    'correoelectronico': None,
                    'selfregistration': None,
                    'cantidad_pruebas_asignadas': None,
                    'cantidad_pruebas_pendientes': None
                }

                campos = ["idcandidato", "nombre", "apellidopaterno", "apellidomaterno", "nombre_completo", 
                          "fechanacimiento", "correoelectronico", "selfregistration", "cantidad_pruebas_asignadas", "cantidad_pruebas_pendientes"]
                df = df_results[campos].copy()
                unique_candidate = df[campos].drop_duplicates()
                unique_candidate["fechanacimiento"] = None if unique_candidate["fechanacimiento"][0] is None else unique_candidate["fechanacimiento"].dt.strftime('%Y-%m-%d').astype(str).replace("nan", None)
                unique_candidate = unique_candidate.to_dict(orient="records")

                for row in unique_candidate:
                    obj_data = {
                        'idcandidato': row.get("idcandidato"),
                        'nombre': row.get("nombre"),
                        'apellidopaterno': row.get("apellidopaterno"),
                        'apellidomaterno': row.get("apellidomaterno"),
                        'nombre_completo': row.get("nombre_completo"),
                        'fechanacimiento': row.get("fechanacimiento"),
                        'correoelectronico': row.get("correoelectronico"),
                        'selfregistration': row.get("selfregistration"),
                        'cantidad_pruebas_asignadas': row.get("cantidad_pruebas_asignadas"),
                        'cantidad_pruebas_pendientes': row.get("cantidad_pruebas_pendientes")
                    }

                logger.debug("Response from candidato.", uid=uid)

                result, flag, message = obj_data, True, 'Se encontró candidato.'
            else:
                flag, message = False, 'No existe candidato.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener datos de los candidato en base de datos {e}'
        finally:
            logger.info("Response from candidato.", uid=uid, message=message)
            return flag, message, result
    