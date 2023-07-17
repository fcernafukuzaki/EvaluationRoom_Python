from configs.resources import db, text
from configs.logging import logger
import pandas as pd


class PsychologicalTestsService():
    """
    Acceso a las pruebas psicológicas.
    """
    
    def get_psychologicaltests(self):
        """
        Descripción:
            Retornar datos de las pruebas psicológicas.
            Retorna las instrucciones, preguntas y alternativas.
        Input:
            - None.
        Output:
            - data
        """
        result = None
        try:
            sql_query = f"""
            SELECT t.idtestpsicologico, t.nombre, t.cantidadpreguntas AS "cantidadpreguntas_total", 
                inst.idparte, inst.instrucciones, inst.alternativamaxseleccion, inst.duracion, inst.cantidadpreguntas, inst.tipoprueba, 
                preg.idpregunta, preg.enunciado, preg.alternativa
            FROM evaluationroom.testpsicologico t
            INNER JOIN evaluationroom.testpsicologicoparte inst ON t.idtestpsicologico=inst.idtestpsicologico
            INNER JOIN evaluationroom.testpsicologicopregunta preg  ON inst.idtestpsicologico=preg.idtestpsicologico AND inst.idparte=preg.idparte
            ORDER BY inst.idtestpsicologico, inst.idparte, preg.idpregunta
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            testpsicologico = db.execute(text(sql_query))

            # Obtén los resultados del cursor como una lista de diccionarios
            results = testpsicologico.fetchall()

            # Convierte los resultados a un DataFrame de pandas
            df_results = pd.DataFrame(results)
            
            # Resultado en formato de lista
            data = []

            df = df_results[["idtestpsicologico", "nombre", "cantidadpreguntas_total"]].copy()
            unique_testpsicologico = df[["idtestpsicologico", "nombre", "cantidadpreguntas_total"]].drop_duplicates()
            # Convierte el DataFrame a un diccionario
            unique_testpsicologico = unique_testpsicologico.to_dict(orient="records")

            df_instrucciones = df_results[["idtestpsicologico", "idparte", "instrucciones", "alternativamaxseleccion", "duracion", "cantidadpreguntas", "tipoprueba"]].copy()
            unique_instrucciones = df_instrucciones[["idtestpsicologico", "idparte", "instrucciones", "alternativamaxseleccion", "duracion", "cantidadpreguntas", "tipoprueba"]].drop_duplicates()
            
            df_preguntas = df_results[["idtestpsicologico", "idparte", "idpregunta", "enunciado", "alternativa"]].copy()
            
            for row in unique_testpsicologico:
                data_test = dict()
                data_test['idtestpsicologico'] = row.get("idtestpsicologico")
                data_test['nombre'] = row.get("nombre")
                data_test['cantidadpreguntas'] = row.get("cantidadpreguntas_total")

                filtro = unique_instrucciones['idtestpsicologico'] == row.get("idtestpsicologico")
                instrucciones = unique_instrucciones[filtro]
                instrucciones = instrucciones.to_dict(orient="records")
                data_instrucciones = []
                for row_instruccion in instrucciones:
                    data_instruccion = dict()
                    data_instruccion["idtestpsicologico"] = row_instruccion.get("idtestpsicologico")
                    data_instruccion["idparte"] = row_instruccion.get("idparte")
                    data_instruccion["instrucciones"] = row_instruccion.get("instrucciones")
                    data_instruccion["alternativamaxseleccion"] = row_instruccion.get("alternativamaxseleccion")
                    data_instruccion["duracion"] = row_instruccion.get("duracion")
                    data_instruccion["cantidadpreguntas"] = row_instruccion.get("cantidadpreguntas")
                    data_instruccion["tipoprueba"] = row_instruccion.get("tipoprueba")
                    
                    data_preguntas = []
                    filtro = ((df_preguntas['idtestpsicologico'] == row_instruccion.get("idtestpsicologico")) & (df_preguntas['idparte'] == row_instruccion.get("idparte")))
                    preguntas = df_preguntas[filtro]
                    preguntas = preguntas.to_dict(orient="records")
                    for row_pregunta in preguntas:
                        data_pregunta = dict()
                        data_pregunta["idtestpsicologico"] = row_pregunta.get("idtestpsicologico")
                        data_pregunta["idparte"] = row_pregunta.get("idparte")
                        data_pregunta["idpregunta"] = row_pregunta.get("idpregunta")
                        data_pregunta["enunciado"] = row_pregunta.get("enunciado")
                        data_pregunta["alternativa"] = row_pregunta.get("alternativa")
                        data_preguntas.append(data_pregunta)
                    
                    data_instruccion['preguntas'] = data_preguntas
                    data_instrucciones.append(data_instruccion)
                    
                data_test['instrucciones'] = data_instrucciones
                data.append(data_test)
            
            logger.debug("Response from pruebas psicológicas.")

            if int(testpsicologico.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró pruebas psicológicas.'
            else:
                code, message = 404, 'No existen pruebas psicológicas.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de las pruebas psicológicas en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
