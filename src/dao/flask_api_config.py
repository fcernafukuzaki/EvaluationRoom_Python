from .flask_config import api
from ..controller.selectionprocess_controller import *

api.add_resource(SelectionProcessController, '/v1/selectionprocess')
