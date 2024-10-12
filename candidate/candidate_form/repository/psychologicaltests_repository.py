import pandas as pd
from configs.resources import db, text
from configs.logging import logger


class PsychologicalTestsRepository():
    """
    Acceso a las pruebas psicológicas.
    """
    
    def get_psychologicaltests_assigned(self, uid:int, idempresa:int):
        """
        Descripción:
            Retornar datos de las pruebas psicológicas asignadas a un candidato.
            El orden de las pruebas psicológicas corresponde a la configuración de una empresa.
        Input:
            - uid:int Identificador del candidato.
            - idempresa:int Identificador de la empresa para obtener la configuración del orden de los tests.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - data Diccionario con un objeto respuesta.
        """
        results = None
        flag = True
        try:
            sql_query = f"""
            SELECT configuracion.idtestpsicologico, configuracion.orden,
                tests.fechaexamen, tests.idparte, tests.idcandidato, tests.duracionestimada
            FROM (
                SELECT (jsonb_array_elements(ec.test_orden->'test_orden')->>'idtestpsicologico')::integer AS idtestpsicologico,
                    (jsonb_array_elements(ec.test_orden->'test_orden')->>'orden')::integer AS orden
                FROM evaluationroom.empresa_configuracion ec 
                WHERE ec.idempresa={idempresa}
                ORDER BY (jsonb_array_elements(ec.test_orden->'test_orden')->>'orden')::integer
            ) AS configuracion
            JOIN (
                SELECT ctest.fechaexamen, inst.idparte, ctest.idcandidato, ctest.idtestpsicologico, inst.duracionestimada
                FROM evaluationroom.candidatotest ctest
                INNER JOIN evaluationroom.testpsicologicoparte inst ON ctest.idtestpsicologico=inst.idtestpsicologico
                WHERE ctest.idcandidato={uid}
            ) AS tests
            ON configuracion.idtestpsicologico=tests.idtestpsicologico
            ORDER BY configuracion.orden ASC, tests.idparte ASC
            """

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                # Resultados del cursor como una lista de diccionarios y convertir a un DataFrame
                result = response_database.fetchall()
                df_results = pd.DataFrame(result)

                campos = ["orden", "fechaexamen", "idparte", "idcandidato", "idtestpsicologico", "duracionestimada"]
                df_results = df_results[campos].drop_duplicates()
                if not df_results["fechaexamen"].isnull().all():
                    df_results["fechaexamen"] = df_results["fechaexamen"].dt.strftime('%Y-%m-%d %H:%M:%S %Z').astype(str).replace("nan", None)
                results = df_results.to_dict(orient="records")

                message = "Operación exitosa"
            else:
                flag, message = False, 'El candidato no tiene pruebas psicológicas asignadas.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener datos de las pruebas psicológicas asignadas al candidato {uid} en base de datos {e}'
        finally:
            return flag, message, results


    def get_psychologicaltests_instructions(self, uid:int, idempresa:int):
        """
        Descripción:
            Retornar las instrucciones de las pruebas psicológicas asignadas a un candidato.
            El orden de las instrucciones de las pruebas psicológicas corresponde a la configuración de una empresa.
        Input:
            - uid:int Identificador del candidato.
            - idempresa:int Identificador de la empresa para obtener la configuración del orden de los tests.
        Output:
            - flag:bool (True, False)
            - message:str Mensaje de la operación.
            - data Diccionario con un objeto respuesta.
        """
        results = None
        flag = True
        try:
            sql_query = f"""
            SELECT configuracion.idtestpsicologico, configuracion.orden,
                tests.idcandidato, 
                tests.fechaexamen,
                tests.nombre, tests.cantidadpreguntas_total, 
                tests.idparte, tests.instrucciones, tests.alternativamaxseleccion, tests.duracion, tests.cantidadpreguntas, tests.tipoprueba, 
                tests.idpregunta, tests.enunciado, tests.alternativa
            FROM (
                SELECT (jsonb_array_elements(ec.test_orden->'test_orden')->>'idtestpsicologico')::integer AS idtestpsicologico,
                    (jsonb_array_elements(ec.test_orden->'test_orden')->>'orden')::integer AS orden
                FROM evaluationroom.empresa_configuracion ec 
                WHERE ec.idempresa={idempresa}
                ORDER BY (jsonb_array_elements(ec.test_orden->'test_orden')->>'orden')::integer
            ) AS configuracion
            JOIN (
                SELECT ctest.idcandidato, 
                    ctest.fechaexamen,
                    t.idtestpsicologico, t.nombre, t.cantidadpreguntas AS "cantidadpreguntas_total", 
                    inst.idparte, inst.instrucciones, inst.alternativamaxseleccion, inst.duracion, inst.cantidadpreguntas, inst.tipoprueba, 
                    preg.idpregunta, preg.enunciado, preg.alternativa
                FROM evaluationroom.testpsicologicopregunta preg
                LEFT JOIN evaluationroom.testpsicologico t ON preg.idtestpsicologico=t.idtestpsicologico
                LEFT JOIN evaluationroom.candidatotest ctest ON preg.idtestpsicologico=ctest.idtestpsicologico
                LEFT JOIN evaluationroom.testpsicologicoparte inst ON preg.idtestpsicologico=inst.idtestpsicologico
                AND preg.idparte=inst.idparte
                WHERE ctest.idcandidato={uid}
                AND CONCAT(preg.idtestpsicologico, '.', preg.idparte, '.', preg.idpregunta) NOT IN (
                        SELECT CONCAT(idtestpsicologico, '.', idparte, '.', idpregunta) 
                        FROM evaluationroom.candidatotestdetalle 
                        WHERE idcandidato = ctest.idcandidato
                        UNION 
                        SELECT CONCAT(ctd.idtestpsicologico, '.', ctd.idparte, '.', ctd.idpregunta) 
                        FROM evaluationroom.testpsicologicopregunta ctd
                        INNER JOIN evaluationroom.testpsicologicoparte tp 
                            ON ctd.idtestpsicologico = tp.idtestpsicologico AND ctd.idparte = tp.idparte
                        WHERE CONCAT(ctd.idtestpsicologico, '.', ctd.idparte) IN (
                            SELECT CONCAT(ct.idtestpsicologico, '.', ct.idparte)
                            FROM evaluationroom.candidatotestdetalle ct
                            WHERE ct.idcandidato = ctest.idcandidato
                            )
                        AND tp.duracion > 0
                        AND tp.tipoprueba <> 'Preg.Abierta'
                        AND CONCAT(ctd.idtestpsicologico, '.', ctd.idparte, '.', ctd.idpregunta) NOT IN (
                            SELECT CONCAT(idtestpsicologico, '.', idparte, '.', idpregunta) 
                            FROM evaluationroom.candidatotestdetalle 
                            WHERE idcandidato = ctest.idcandidato
                    )
                )
            ) AS tests
            ON configuracion.idtestpsicologico=tests.idtestpsicologico
            ORDER BY configuracion.orden ASC, tests.idparte, tests.idpregunta
            """

            # Ejecutar la consulta SQL
            response_database = db.execute(text(sql_query))

            if int(response_database.rowcount) > 0:
                # Resultados del cursor como una lista de diccionarios y convertir a un DataFrame
                result = response_database.fetchall()
                df_results = pd.DataFrame(result)
                
                campos = ["orden", "idtestpsicologico", "idparte", "instrucciones", "alternativamaxseleccion", "duracion", "cantidadpreguntas", "tipoprueba"]
                df_instrucciones = df_results[campos].copy()
                unique_instrucciones = df_instrucciones[campos].drop_duplicates()
                instrucciones = unique_instrucciones.to_dict(orient="records")
                data_instrucciones = []

                data_instrucciones = [
                    {
                        "orden": row_instruccion.get("orden"),
                        "idtestpsicologico": row_instruccion.get("idtestpsicologico"),
                        "idparte": row_instruccion.get("idparte"),
                        "instrucciones": row_instruccion.get("instrucciones"),
                        "alternativamaxseleccion": row_instruccion.get("alternativamaxseleccion"),
                        "duracion": row_instruccion.get("duracion"),
                        "cantidadpreguntas": row_instruccion.get("cantidadpreguntas"),
                        "tipoprueba": row_instruccion.get("tipoprueba")
                    }
                    for row_instruccion in instrucciones
                ]

                campos = ["orden", "idtestpsicologico", "idparte", "idpregunta", "alternativa", "enunciado"]
                df_preguntas_pendientes = df_results[campos].copy()
                preguntas_pendientes = df_preguntas_pendientes.to_dict(orient="records")
                data_preguntas_pendientes = []

                data_preguntas_pendientes = [
                    {
                        "orden": row.get("orden"),
                        "idtestpsicologico": row.get("idtestpsicologico"),
                        "idparte": row.get("idparte"),
                        "idpregunta": row.get("idpregunta"),
                        "alternativa": row.get("alternativa"),
                        "enunciado": row.get("enunciado")
                    }
                    for row in preguntas_pendientes
                ]

                results = {
                    "testpsicologicos_instrucciones": data_instrucciones,
                    "preguntas_pendientes": data_preguntas_pendientes
                }

                message = "Operación exitosa"
            else:
                flag, message = False, 'No existen pruebas psicológicas.'
        except Exception as e:
            logger.error("Error.", error=e)
            db.rollback()
            flag, message = False, f'Hubo un error al obtener las instrucciones de las pruebas psicológicas en base de datos {e}'
        finally:
            return flag, message, results
