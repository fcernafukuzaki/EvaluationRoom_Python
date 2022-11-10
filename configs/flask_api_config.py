from .flask_config import api
from controller.candidate_info_controller import *
from controller.selectionprocess_controller import *
from controller.selectionprocess_candidate_controller import *
from controller.selection_process.client_controller import *
from controller.selection_process.jobposition_controller import *
from controller.jobposition_candidate_controller import *
from controller.candidate_without_selectionprocess_controller import *
from controller.candidate_resettest_controller import *
from controller.candidate_form.candidate_controller import *
from controller.candidate_form.ubigeo_controller import *
from controller.candidate_form.sexo_controller import *
from controller.candidate_form.documento_identidad_controller import *
from controller.candidate_form.estado_civil_controller import *
from controller.candidate_form.tipo_direccion_controller import *
from controller.candidate_form.psychologicaltest_controller import *
from controller.login_user.login_user_controller import *
from controller.api.api import *
from controller.menu.psychologicaltests_controller import *
from controller.soporte_tecnico.candidato_soportetecnico_notificacion_controller import *
from controller.candidate_email_validate.candidatoemailvalidar_controller import *
from controller.recruiter.reclutadoridentificadorvalidar_controller import *
from controller.recruiter.reclutadoremailvalidar_controller import *
from controller.administrator.usuarios_controller import *
from controller.administrator.perfiles_controller import *

api.add_resource(LoginUserController, 
    '/login/authenticate')

api.add_resource(CandidateController, 
    '/v1/candidate',
    '/v1/candidate/self_registered=<string:self_registered>',
    '/v1/candidate/uid=<int:uid>',
    '/v1/candidate/email=<string:email>')

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

api.add_resource(ClientController, 
    '/v1/clients/',
    '/v1/clients/<int:uid>')

api.add_resource(JobPositionController, 
    '/v1/jobposition/',
    '/v1/jobposition/<int:idclient>',
    '/v1/jobposition/<int:idclient>/<int:idjobposition>')

api.add_resource(JobPositionCandidateController, 
    '/v1/jobpositioncandidate',
    '/v1/jobpositioncandidate/<int:idclient>/<int:idjobposition>',
    '/v1/jobpositioncandidate/<int:idclient>/<int:idjobposition>/<int:idcandidate>')

api.add_resource(CandidateResetTestController, 
    '/v1/candidate/resettest')

# Completar valores para formulario de registro de candidato
api.add_resource(UbigeoController, 
    '/v1/candidateform/ubigeo',
    '/v1/candidateform/ubigeo/<int:idcountry>',
    '/v1/candidateform/ubigeo/<int:idcountry>/<int:iddepartamento>',
    '/v1/candidateform/ubigeo/<int:idcountry>/<int:iddepartamento>/<int:idprovincia>')

api.add_resource(SexoController, 
    '/v1/candidateform/sexo')

api.add_resource(DocumentoIdentidadController, 
    '/v1/candidateform/documentoidentidad')

api.add_resource(EstadoCivilController, 
    '/v1/candidateform/estadocivil')

api.add_resource(TipoDireccionController, 
    '/v1/candidateform/tipodireccion')

api.add_resource(PsychologicalTestController, 
    '/v1/candidateform/testpsicologicos')

# Menu reclutador
api.add_resource(PsychologicalTestsController,
    '/v1/candidateform/testpsicologicos/info/email=<string:email>')

# Obtener interpretación de las pruebas psicológicas
api.add_resource(PsychologicalTestInterpretacionController, 
    '/testpsicologico/interpretacion/candidato/<int:idcandidato>',
    '/testpsicologico/download/informe/uid=<int:uid>&email=<string:email>&token=<string:token>')

api.add_resource(CandidatoSoporteTecnicoNotificacionController,
    '/v1/candidato_soportetecnico_notificar')

api.add_resource(CandidatoEmailValidarController,
    '/candidato_email_validar')

"""
Eliminar luego de migrar código fuente.
"""
api.add_resource(ReclutadorIdentificadorValidarController,
    '/reclutador_identificador_validar')

api.add_resource(ReclutadorEmailValidarController,
    '/reclutador_email_validar')

# Administrador accesos gestionar
api.add_resource(UsuariosController, 
    '/usuarios/',
    '/usuarios/<int:uid>')

api.add_resource(PerfilesController, 
    '/perfiles/',
    '/perfiles/<int:uid>')
