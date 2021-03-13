from ..flask_config import db, ma
from .client import Client
from .jobposition import JobPosition

class ClientInfo():
    all_clients_resumen = db.session.query(
                    Client.idcliente, 
                    Client.nombre,
                    db.func.count(Client.idcliente).label('cant_puestos_laborales'),
                ).outerjoin(JobPosition, JobPosition.idcliente==Client.idcliente).group_by(Client.idcliente).order_by(Client.idcliente)
            
class ClientInfoSchema(ma.Schema):
    class Meta:
        fields = ('cant_puestos_laborales', 'idcliente', 'nombre')
