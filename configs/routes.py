from authorization.login_user_controller import LoginUserController

# from controller.candidate_info_controller import CandidateInfoSimpleController
# from controller.selectionprocess_controller import *
# from controller.selectionprocess_candidate_controller import *
# from controller.selection_process.client_controller import *
# from controller.selection_process.jobposition_controller import *
# from controller.jobposition_candidate_controller import *
# from controller.candidate_resettest_controller import *
# from controller.candidate_form.candidate_controller import *
# from controller.api.api_test_interpretacion import *
# from controller.soporte_tecnico.candidato_soportetecnico_notificacion_controller import *
# from controller.candidate_email_validate.candidatoemailvalidar_controller import *
# from controller.recruiter.reclutadoridentificadorvalidar_controller import *
# from controller.recruiter.reclutadoremailvalidar_controller import *
from administration.usuarios_controller import UsuariosController
from administration.perfiles_controller import PerfilesController
from administration.psychologicaltests_controller import PsychologicalTestsController
from dashboard.dashboard import Dashboard
from controller.candidate_form.ubigeo_controller import UbigeoController
from controller.candidate_form.sexo_controller import SexoController
from controller.candidate_form.documento_identidad_controller import DocumentoIdentidadController
from controller.candidate_form.estado_civil_controller import EstadoCivilController
from controller.candidate_form.tipo_direccion_controller import TipoDireccionController
from controller.candidate_form.psychologicaltest_controller import PsychologicalTestController
from controller.candidate_form.candidate_controller import CandidateController


def api_add_resource(api):
    # Agregar la clase como un recurso a la API
    api.add_resource(LoginUserController, "/login/authenticate")

    # api.add_resource(CandidateController, 
    #     "/api/v1/candidates",
    #     "/api/v1/candidates/self_registered=<string:self_registered>",
    #     "/api/v1/candidates/uid=<int:uid>",
    #     "/api/v1/candidates/email=<string:email>")

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

    # api.add_resource(CandidateResetTestController, 
    #     "/v1/candidate/resettest")

    # Completar valores para formulario de registro de candidato
    api.add_resource(UbigeoController, 
        "/api/v1/candidates/fields/ubigeo",
        "/api/v1/candidates/fields/ubigeo/pais=<int:idcountry>",
        "/api/v1/candidates/fields/ubigeo/pais=<int:idcountry>&departamento=<int:iddepartamento>",
        "/api/v1/candidates/fields/ubigeo/pais=<int:idcountry>&departamento=<int:iddepartamento>&provincia=<int:idprovincia>")

    api.add_resource(SexoController, 
        "/api/v1/candidates/fields/sexos")

    api.add_resource(DocumentoIdentidadController, 
        "/api/v1/candidates/fields/documentosidentidad")

    api.add_resource(EstadoCivilController, 
        "/api/v1/candidates/fields/estadosciviles")

    api.add_resource(TipoDireccionController, 
        "/api/v1/candidates/fields/tiposdirecciones")

    api.add_resource(PsychologicalTestController, 
        "/api/v1/candidates/fields/testpsicologicos")
    
    api.add_resource(CandidateController, 
        "/api/v1/candidates/fields/self_registered=<string:self_registered>",
        "/api/v1/candidates/<int:uid>/fields",
        "/api/v1/candidates/fields/numerodocumentoidentidad=<string:numerodocumentoidentidad>")

    # # Obtener interpretación de las pruebas psicológicas
    # api.add_resource(PsychologicalTestInterpretacionController, 
    #     "/testpsicologico/interpretacion/candidato/<int:idcandidato>",
    #     "/testpsicologico/download/informe/uid=<int:uid>&email=<string:email>&token=<string:token>")

    # api.add_resource(CandidatoSoporteTecnicoNotificacionController,
    #     "/v1/candidato_soportetecnico_notificar")

    # api.add_resource(CandidatoEmailValidarController,
    #     "/candidato_email_validar")

    # """
    # Eliminar luego de migrar código fuente.
    # """
    # api.add_resource(ReclutadorIdentificadorValidarController,
    #     "/reclutador_identificador_validar")

    # api.add_resource(ReclutadorEmailValidarController,
    #     "/reclutador_email_validar")

    # Administrador gestionar accesos
    api.add_resource(UsuariosController, 
        "/api/v1/usuarios/",
        "/api/v1/usuarios/<int:uid>"
        )

    api.add_resource(PerfilesController, 
        "/api/v1/perfiles/",
        "/api/v1/perfiles/<int:uid>"
        )
    
    # Menu reclutador
    api.add_resource(PsychologicalTestsController,
        "/api/v1/candidateform/testpsicologicos/info")
    
    # Dashboard
    api.add_resource(Dashboard, 
        "/api/v1/dashboard/email=<string:email>")
