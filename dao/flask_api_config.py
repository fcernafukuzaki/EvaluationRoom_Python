from .flask_config import api
from ..controller.candidate_controller import *
from controller.candidate_info_controller import *
from controller.selectionprocess_controller import *
from controller.selectionprocess_candidate_controller import *
from controller.client_controller import *
from controller.client_info_controller import *
from controller.jobposition_controller import *
from controller.jobposition_candidate_controller import *
from controller.candidate_without_selectionprocess_controller import *

api.add_resource(CandidateController, 
    '/v1/candidate',
    '/v1/candidate/<int:idcandidate>')

api.add_resource(CandidateInfoSimpleController, 
    '/v1/candidate_info')

api.add_resource(SelectionProcessController, 
    '/v1/selectionprocess',
    '/v1/selectionprocess/<string:process_status>',
    '/v1/selectionprocess/<int:idclient>/<int:idjobposition>')

api.add_resource(SelectionProcessCandidateController, 
    '/v1/selectionprocesscandidate',
    '/v1/selectionprocesscandidate/<int:idclient>',
    '/v1/selectionprocesscandidate/<int:idclient>/<int:idjobposition>')

api.add_resource(CandidateWithoutSelectionProcessController, 
    '/v1/candidatewithoutselectionprocess')

api.add_resource(ClientInfoSimpleController, 
    '/v1/client_info')

api.add_resource(ClientController, 
    '/v1/client',
    '/v1/client/<int:idclient>')

api.add_resource(JobPositionController, 
    '/v1/jobposition',
    '/v1/jobposition/<int:idclient>',
    '/v1/jobposition/<int:idclient>/<int:idjobposition>')

api.add_resource(JobPositionCandidateController, 
    '/v1/jobpositioncandidate',
    '/v1/jobpositioncandidate/<int:idclient>/<int:idjobposition>',
    '/v1/jobpositioncandidate/<int:idclient>/<int:idjobposition>/<int:idcandidate>')
