from configs.resources import db
from objects.psychologicaltest import PsychologicalTest, PsychologicalTestInfoSchema

psychologicaltest_info_schema = PsychologicalTestInfoSchema(many=True)

class PsychologicalTestsService():
    
    def get_psychologicaltests(self):
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