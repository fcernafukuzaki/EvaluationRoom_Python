from configs.logging import logger
from administration.repository.psychologicaltests_repository import PsychologicalTestsRepository


psychologicaltests_repository = PsychologicalTestsRepository()


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
            - result:object Lista de pruebas psicológicas.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            flag, message, result = psychologicaltests_repository.get_all()
            code = 200 if flag else 404
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de las pruebas psicológicas en base de datos {e}'
        finally:
            logger.info(message)
            return result, code, message
