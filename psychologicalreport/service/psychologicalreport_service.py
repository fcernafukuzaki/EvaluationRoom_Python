from __future__ import annotations
import psycopg2
import json
from flask import send_file
from configs.logging import logger
from psychologicalreport.repository.testpsicologico_autoevalansiedadaer_repository import TestPsicologicoAutoevalAnsiedadAER
from psychologicalreport.repository.testpsicologico_gatb_repository import TestPsicologicoGATB
from psychologicalreport.repository.testpsicologico_disc_repository import TestPsicologicoDISC
from psychologicalreport.repository.candidato_repository import Candidato
from psychologicalreport.service.testpsicologico_context import TestPsicologicoContext
from psychologicalreport.repository.informepsicologico_repository import InformePsicologico
from authorization.authorizer_service import AuthorizerService

authorizer_service = AuthorizerService()

PATH_FILE_TEST = "psychologicalreport/templates/AUTOEVALUACION ANSIEDAD ESTADO-RASGO.xlsx"
PATH_FILE_TEST_INFORME = "psychologicalreport/templates/INFORME PSICOLOGICO_template.docx"

# Establecer la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
)

class PsychologicalTestReportService():

    def create(self, idcandidato:int):
        """
        Descripción:
            Interpretar los resultados de las pruebas psicológicas.
        Input:
            - idcandidato:int Identificador del candidato/paciente.
        
        Output:
            - result:object Mensaje.
            - code:int Código de respuesta. [200:OK, 404:Not Found, 503:Error]
            - message:str Mensaje de salida.
        """
        result = None
        try:
            file = PATH_FILE_TEST
            
            candidato = Candidato(conn, idcandidato)
            testspsicologicos = candidato.get_testspsicologicos()
            data = candidato.data()
            logger.debug("El candidato tiene asignada las pruebas:", uid=idcandidato, testspsicologicos=testspsicologicos)

            # Obtener datos para el informe psicológico

            result = data.to_dict(orient='records')[0]
            is_male = candidato.is_male()

            for test in testspsicologicos:
                idtestpsicologico = test["idtestpsicologico"]

                test_to_instance = {
                    "2": TestPsicologicoGATB(conn, file, idcandidato),
                    "3": TestPsicologicoDISC(conn, file, idcandidato),
                    "7": TestPsicologicoAutoevalAnsiedadAER(conn, file, is_male, idcandidato),
                }
                instance = test_to_instance.get(str(idtestpsicologico), None) # None -> "unknown"
                
                testpsicologico_context = TestPsicologicoContext(None)

                if instance:
                    testpsicologico_context.strategy = instance
                    resultado = testpsicologico_context.add_data_report(result)
                    result = resultado

            file_name = result.get("file_name")

            path_template = PATH_FILE_TEST_INFORME
            path_informe = f"INFORME PSICOLOGICO_{file_name}.docx"

            informe = InformePsicologico(path_template, path_informe)
            informe.replace(result)
            informe.save()

            logger.debug("Resultados del candidato:", uid=idcandidato, result=json.dumps(result, indent=4))
            code, message = 200, 'OK'
        except Exception as e:
            logger.error("Error service.", uid=idcandidato, error=e)
            code, message = 503, f'Hubo un error al generar la interpretación {e}'
        finally:
            logger.info("Response from generate interpretation.", uid=idcandidato, message=message)
            return result, code, message


    def download(self, uid:int, email:str, token:str):
        """
        Descripción:
            Descargar el informe psicológico.
        Input:
            - idcandidato:int Identificador del candidato/paciente.
            - email:str Correo electrónico.
            - token:str Hash recuperado por servicio de autenticación.
        Output:
            - result:object Archivo.
        """
        result = None
        try:
            if uid:
                flag, respuesta, codigo, _ = authorizer_service.validate_recruiter_identify(token, email)
                
                if flag:

                    idcandidato = uid
                    candidato = Candidato(conn, idcandidato)
                    data = candidato.data()
                    result = data.to_dict(orient='records')[0]
                    file_name = result.get("file_name")
                    path_informe = f"INFORME PSICOLOGICO_{file_name}.docx"
                    logger.debug("Descargar el informe del candidato.", uid=idcandidato, path_informe=path_informe)
                    
                    mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    return send_file(path_informe, mimetype=mimetype, as_attachment=True, download_name=path_informe)
        except Exception as e:
            logger.error("Error service.", uid=uid, error=e)
            return None