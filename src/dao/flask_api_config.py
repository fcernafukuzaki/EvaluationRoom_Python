from .flask_config import api
from controller.candidate_controller import *
from controller.selectionprocess_controller import *
from controller.selectionprocess_candidate_controller import *

api.add_resource(CandidateController, 
    '/v1/candidate',
    '/v1/candidate/<int:idcandidate>')

api.add_resource(SelectionProcessController, 
    '/v1/selectionprocess',
    '/v1/selectionprocess/<int:idclient>',
    '/v1/selectionprocess/<int:idclient>/<int:idjobposition>')

api.add_resource(SelectionProcessCandidateController, 
    '/v1/selectionprocesscandidate',
    '/v1/selectionprocesscandidate/<int:idclient>',
    '/v1/selectionprocesscandidate/<int:idclient>/<int:idjobposition>')
