from configs.resources import db
from objects.psychologicaltest import PsychologicalTest, PsychologicalTestSchema

psychologicaltest_schema = PsychologicalTestSchema(many=True)

class PsychologicalTestService():
    
    def get_psychologicaltests(self):
        all_psychologicaltests = PsychologicalTest.query.all()
        if all_psychologicaltests:
            message = 'Se encontraron registros en base de datos.'
            return psychologicaltest_schema.dump(all_psychologicaltests), 200, message
        message = 'No se encontraron registros en base de datos.'
        return None, 404, message