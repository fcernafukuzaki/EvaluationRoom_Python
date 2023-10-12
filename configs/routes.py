from authorization.login_user_controller import LoginUserController

# from controller.candidate_info_controller import CandidateInfoSimpleController
# from controller.selectionprocess_controller import *
# from controller.selectionprocess_candidate_controller import *
# from controller.selection_process.client_controller import *
# from controller.selection_process.jobposition_controller import *
# from controller.jobposition_candidate_controller import *
# from controller.candidate_form.candidate_controller import *
from administration.controller.usuarios_controller import UsuariosController
from administration.controller.perfiles_controller import PerfilesController
from administration.controller.psychologicaltests_controller import PsychologicalTestsController
from dashboard.dashboard import Dashboard
from candidate.candidate_form.controller.ubigeo_controller import UbigeoController
from candidate.candidate_form.controller.sexo_controller import SexoController
from candidate.candidate_form.controller.documento_identidad_controller import DocumentoIdentidadController
from candidate.candidate_form.controller.estado_civil_controller import EstadoCivilController
from candidate.candidate_form.controller.tipo_direccion_controller import TipoDireccionController
from candidate.candidate_form.controller.psychologicaltest_controller import PsychologicalTestController
from candidate.candidate_form.controller.candidate_controller import CandidateController
from candidate.candidate_form.controller.candidate_form_controller import CandidateFormController
from soporte_tecnico.controller.candidato_soportetecnico_notificacion_controller import CandidatoSoporteTecnicoNotificacionController
from evaluations.controller.evaluation_controller import EvaluationController
from evaluations.controller.log_controller import LogController
from evaluations.controller.respuesta_controller import RespuestaController
from psychologicalreport.controller.psychologicalreport_controller import PsychologicalTestInterpretacionController
from evaluations.controller.candidate_resettest_controller import CandidateResetTestController

def api_add_resource(api):
    # Autenticación de usuario
    api.add_resource(LoginUserController, "/login/authenticate")

    # Completar valores para formulario de registro de candidato
    api.add_resource(
        UbigeoController,
        "/api/v1/candidates/fields/ubigeo",
        "/api/v1/candidates/fields/ubigeo/pais=<int:idcountry>",
        "/api/v1/candidates/fields/ubigeo/pais=<int:idcountry>&departamento=<int:iddepartamento>",
        "/api/v1/candidates/fields/ubigeo/pais=<int:idcountry>&departamento=<int:iddepartamento>&provincia=<int:idprovincia>",
    )

    api.add_resource(SexoController, "/api/v1/candidates/fields/sexos")

    api.add_resource(
        DocumentoIdentidadController, "/api/v1/candidates/fields/documentosidentidad"
    )

    api.add_resource(EstadoCivilController, "/api/v1/candidates/fields/estadosciviles")

    api.add_resource(
        TipoDireccionController, "/api/v1/candidates/fields/tiposdirecciones"
    )

    api.add_resource(
        PsychologicalTestController, "/api/v1/candidates/fields/testpsicologicos"
    )

    api.add_resource(
        CandidateFormController,
        "/api/v1/candidates/fields/self_registered=<string:self_registered>",
        "/api/v1/candidates/<int:uid>/fields",
        "/api/v1/candidates/fields/numerodocumentoidentidad=<string:numerodocumentoidentidad>",
        "/api/v1/candidates/fields/email=<string:email>",
    )

    api.add_resource(CandidateController, "/api/v1/candidates/<int:uid>")

    # Notificación de errores a soporte técnico
    api.add_resource(
        CandidatoSoporteTecnicoNotificacionController,
        "/api/v1/candidates/notificarsoportetecnico",
        "/api/v1/candidates/notificarsoportetecnico/type=<string:type>",
    )

    # Evaluación de candidato
    api.add_resource(EvaluationController, "/api/v1/evaluations")

    # Log de evaluación de candidato
    api.add_resource(LogController, "/api/v1/evaluations/actions")

    api.add_resource(RespuestaController, "/api/v1/evaluations/answers")

    # Administrador gestionar accesos
    api.add_resource(
        UsuariosController, "/api/v1/usuarios/", "/api/v1/usuarios/<int:uid>"
    )

    api.add_resource(
        PerfilesController, "/api/v1/perfiles/", "/api/v1/perfiles/<int:uid>"
    )

    # Menu reclutador
    api.add_resource(
        PsychologicalTestsController, "/api/v1/candidateform/testpsicologicos/info"
    )

    # Dashboard
    api.add_resource(Dashboard, "/api/v1/dashboard/email=<string:email>")

    # Obtener interpretación de las pruebas psicológicas
    api.add_resource(PsychologicalTestInterpretacionController,
        "/api/v1/psychologicalreport/interpretacion/candidato/<int:idcandidato>",
        "/api/v1/psychologicalreport/download/uid=<int:uid>&email=<string:email>&token=<string:token>")
    
    # Resetear preguntas de una prueba psicológica
    api.add_resource(CandidateResetTestController, "/api/v1/candidates/resettest")

    # api.add_resource(CandidateInfoSimpleController,
    #     "/v1/candidate_info")

    # api.add_resource(SelectionProcessController,
    #     "/v1/selectionprocess",
    #     "/v1/selectionprocess/<string:process_status>",
    #     "/v1/selectionprocess/<int:idclient>/<int:idjobposition>")

    # api.add_resource(SelectionProcessCandidateController,
    #     "/v1/selectionprocesscandidate",
    #     "/v1/selectionprocesscandidate/<int:idclient>",
    #     "/v1/selectionprocesscandidate/<int:idclient>/<int:idjobposition>")

    # api.add_resource(ClientController,
    #     "/v1/clients/",
    #     "/v1/clients/<int:uid>")

    # api.add_resource(JobPositionController,
    #     "/v1/jobposition/",
    #     "/v1/jobposition/<int:idclient>",
    #     "/v1/jobposition/<int:idclient>/<int:idjobposition>")

    # api.add_resource(JobPositionCandidateController,
    #     "/v1/jobpositioncandidate",
    #     "/v1/jobpositioncandidate/<int:idclient>/<int:idjobposition>",
    #     "/v1/jobpositioncandidate/<int:idclient>/<int:idjobposition>/<int:idcandidate>")
