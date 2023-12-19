from flask_restful import Resource
from common.util import get_response_body
from configs.logging import logger
from psychologicalreport.api.api_test_interpretacion_service import PsychologicalTestInterpretacionService
from psychologicalreport.service.psychologicalreport_service import PsychologicalTestReportService


psychologicaltestinterpretacion_service = PsychologicalTestInterpretacionService()
psychologicaltestreport_service = PsychologicalTestReportService()


class PsychologicalTestInterpretacionController(Resource):
    
    def get(self, idcandidato:int=None, uid:int=None, email:str=None, token:str=None, model:str=1):
        """ 
        Descripción:
            Obtener y generar la interpretación de las pruebas psicológicas.
            Si se envía el idcandidato, entonces se genera la interpretación de los resultados de las pruebas.
            Si se envía el uid, entonces se descarga el informe psicológico.
        Input:
            - idcandidato:int Identificador del candidato/paciente.
            - uid:int Identificador del candidato/paciente de quien se va a descargar su informe.
            - email:str Correo electrónico del usuario que realiza la operación.
            - token:str Token del usuario que realiza la operación.
            - model:str Modelo de informe psicológico. [1:Informe consultora, 2:Informe clínica]
        Output:
            - result:object Archivo .docx.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
        """
        response_body = None
        try:
            logger.debug("PsychologicalTestInterpretacionController", idcandidato=idcandidato, uid=uid, email=email, model=model)
            
            if idcandidato:
                model_dict = {
                    1: psychologicaltestinterpretacion_service.create(idcandidato),
                    2: psychologicaltestreport_service.create(idcandidato)
                }

                # result, code, message = psychologicaltestinterpretacion_service.create(idcandidato)
                result, code, message = model_dict.get(model, None)
                response_body = {"mensaje": result} if result else None
                return get_response_body(code=200, message="OK", user_message="OK", body=response_body), 200
            
            if uid:
                model_dict = {
                    1: psychologicaltestinterpretacion_service.download(uid, email, token),
                    2: psychologicaltestreport_service.download(uid, email, token)
                }
                return model_dict.get(model, None)
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener la interpretación {e}'
            user_message = message
            return get_response_body(code=code, message=message, user_message=user_message), code
