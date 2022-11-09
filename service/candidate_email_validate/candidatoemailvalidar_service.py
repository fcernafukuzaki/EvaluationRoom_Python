from configs.flask_config import db
from objects.candidate import Candidate, CandidateEmailValidateSchema

candidato_schema = CandidateEmailValidateSchema()


class CandidatoEmailValidarService():

    def valida_email(self, email):
        email_valido, mensaje, candidato = self.valida_email_candidato(email)
        
        if not email_valido:
            return {'mensaje': mensaje}, 404
        return candidato_schema.jsonify(candidato)

    def valida_email_candidato(self, email):
        candidato = db.session.query(Candidate).filter(Candidate.correoelectronico==email)
        if candidato.count():
            print('Se encontró candidato con el correo electronico {}'.format(email))
            return True, 'Existe candidato', candidato.one()
        print('No existe candidato con el correo electronico {}'.format(email))
        return False, 'No existe candidato.', None
