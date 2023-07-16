from configs.resources import db, text
from configs.logging import logger


class PsychologicalTestsService():
    """
    Acceso a las pruebas psicológicas.
    """
    
    def get_psychologicaltests(self):
        """
        Descripción:
            Retornar datos de las pruebas psicológicas.
        Input:
            - None.
        Output:
            - data
        """
        result = None
        try:
            sql_query = f"""
            SELECT t.idtestpsicologico, t.nombre, t.cantidadpreguntas, inst.idparte, inst.instrucciones, inst.alternativamaxseleccion, inst.duracion, inst.cantidadpreguntas, inst.tipoprueba, preg.idpregunta, preg.enunciado, preg.alternativa
            FROM evaluationroom.testpsicologico t
            INNER JOIN evaluationroom.testpsicologicoparte inst ON t.idtestpsicologico=inst.idtestpsicologico
            INNER JOIN evaluationroom.testpsicologicopregunta preg  ON inst.idtestpsicologico=preg.idtestpsicologico AND inst.idparte=preg.idparte
            ORDER BY inst.idtestpsicologico, inst.idparte, preg.idpregunta
            """

            # Ejecutar la consulta SQL y obtener los resultados en un dataframe
            usuarios = db.execute(text(sql_query))

            # Resultado en formato de lista
            data = []

            for row in usuarios:
                data_usuario = dict()
                data_usuario['idUsuario'] = row.idusuario
                data_usuario['activo'] = row.activo
                data_usuario['correoElectronico'] = row.correoelectronico
                data_usuario['nombre'] = row.nombre
                data.append(data_usuario)
            
            logger.debug("Response from pruebas psicológicas.")

            if int(usuarios.rowcount) > 0:
                result, code, message = data, 200, 'Se encontró pruebas psicológicas.'
            else:
                code, message = 404, 'No existen pruebas psicológicas.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de las pruebas psicológicas en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
        

        result, code, message = None, 404, 'No se encontraron registros en base de datos.'
        try:
            all_psychologicaltests = PsychologicalTest.query.all()
            if all_psychologicaltests:
                message = 'Se encontraron registros en base de datos.'
                result, code, message = psychologicaltest_info_schema.dump(all_psychologicaltests), 200, message
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de puesto laboral en base de datos {e}'
        finally:
            print(message)
            return result, code, message