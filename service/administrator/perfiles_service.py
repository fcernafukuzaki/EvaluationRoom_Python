from configs.flask_config import db
from objects.perfil import Perfil, PerfilSchema

perfil_schema = PerfilSchema()
perfiles_schema = PerfilSchema(many=True)

class PerfilesService():

    def get_perfiles(self):
        result = None
        try:
            perfiles = db.session.query(Perfil).order_by(Perfil.idperfil)

            if perfiles.count():
                result, code, message = perfiles_schema.dump(perfiles), 200, 'Se encontró perfiles.'
            else:
                code, message = 404, 'No existen perfiles.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de perfiles en base de datos {e}'
        finally:
            print(message)
            return result, code, message
    
    def get_perfil(self, uid):
        result = None
        try:
            perfil = db.session.query(Perfil).filter(Perfil.idperfil==uid).all()
            
            if perfil:
                result, code, message = perfil_schema.dump(perfil[0]), 200, 'Se encontró perfil.'
            else:
                code, message = 404, 'No existe perfil.'
        except Exception as e:
            code, message = 503, f'Hubo un error al obtener datos de perfil {uid} en base de datos {e}'
        finally:
            print(message)
            return result, code, message
    
    def add_perfil(self, nombre):
        result = None
        try:
            new_perfil = Perfil(nombre=nombre)
            db.session.add(new_perfil)
            db.session.commit()
            db.session.refresh(new_perfil)
            result = new_perfil.idperfil
            code, message = 200, 'Se registró perfil en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al registrar perfil en base de datos {e}'
        finally:
            print(message)
            return result, code, message
    
    def update_perfil(self, uid, nombre):
        result = None
        try:
            update_perfil = Perfil.query.get((uid))
            update_perfil.nombre = nombre
            db.session.commit()
            result, code, message = uid, 200, 'Se actualizó perfil en base de datos.'
        except Exception as e:
            code, message = 503, f'Hubo un error al actualizar perfil en base de datos {e}'
        finally:
            print(message)
            return result, code, message
