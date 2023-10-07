import re
import urllib3


# def str2bool(v):
#     """Retorna un Boolean a partir de un palabra que se encuentre en la lista"""
#     return v.lower() in ("yes", "true", "t", "1")


# def field_in_dict(dictionary, field):
#     if field in dictionary:
#         return True
#     return False


def get_response_body(code=200, message="OK", user_message="", body=None):
    if re.match(r"^2\d{2}$", str(code)):
        return {
            "code": code,
            "message": message,
            "user_message": user_message,
            "body": body,
        }
    return {"error": {"code": code, "message": message, "user_message": user_message}}


def invoke_api(url, body, headers={"Content-Type": "application/json"}, method="POST", retries=False):
    http = urllib3.PoolManager()
    response = http.request(method, url, body=body, headers=headers, retries=retries)
    return response


def seconds_to_format(segundos):
    """ Mostrar la cantidad de horas y minutos que tomarán todas las pruebas psicológicas.
    """
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    
    return f"{horas} hora(s) y {minutos} minutos"
