import re
import urllib3


def obtener_header(request_headers):
    ''' Obtener datos del header.
    '''
    origin = request_headers.get('Origin')
    host = request_headers.get('Host')
    user_agent = request_headers.get('User-Agent')
    
    return origin, host, user_agent


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
