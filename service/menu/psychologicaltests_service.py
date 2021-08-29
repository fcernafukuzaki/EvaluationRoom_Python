from configs.flask_config import db
from objects.psychologicaltest import PsychologicalTest, PsychologicalTestInfoSchema

psychologicaltest_info_schema = PsychologicalTestInfoSchema(many=True)

class PsychologicalTestsService():
    
    def get_psychologicaltests(self):
        all_psychologicaltests = PsychologicalTest.query.all()
        if all_psychologicaltests:
            message = 'Se encontraron registros en base de datos.'
            return psychologicaltest_info_schema.dump(all_psychologicaltests), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message