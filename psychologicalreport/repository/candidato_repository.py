from datetime import datetime
import pandas as pd


class Candidato():
    def __init__(self, conn, idcandidato:int):
        self.conn = conn
        self.idcandidato = idcandidato


    def __calcular_edad(self, fecha_nacimiento):
        fecha_actual = datetime.now()
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
        edad = fecha_actual.year - fecha_nacimiento.year
        if fecha_actual.month < fecha_nacimiento.month:
            edad -= 1
        elif fecha_actual.month == fecha_nacimiento.month and fecha_actual.day < fecha_nacimiento.day:
            edad -= 1
        return edad


    def is_male(self):
        sql_query = f"""
        SELECT CASE WHEN s.nombre = 'MASCULINO' THEN true ELSE false END AS "Genero"
        FROM evaluationroom.candidato c
        INNER JOIN evaluationroom.sexo s ON c.idsexo=s.idsexo
        WHERE idcandidato={self.idcandidato}
        """
        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        data = pd.read_sql_query(sql_query, self.conn)
        return data["Genero"].values.tolist()[0]


    def get_testspsicologicos(self):
        sql_query = f"""
        SELECT ct.idtestpsicologico
        FROM evaluationroom.candidato c
        INNER JOIN evaluationroom.candidatotest ct ON ct.idcandidato=c.idcandidato
        WHERE c.idcandidato={self.idcandidato}
        ORDER BY c.idcandidato DESC
        """
        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        data = pd.read_sql_query(sql_query, self.conn)

        return data.to_dict(orient='records')


    def data(self):
        sql_query = f"""
        SELECT apellidopaterno AS "apellidopaterno", apellidomaterno AS "apellidomaterno", c.nombre AS "nombre",
        numerodocumentoidentidad AS "dni",
        TO_CHAR(fechanacimiento, 'DD/MM/YYYY') AS "fecha_nacimiento",
        ec.nombre AS "estado_civil"
        FROM evaluationroom.candidato c
        INNER JOIN evaluationroom.estadocivil ec ON c.idestadocivil=ec.idestadocivil
        WHERE idcandidato={self.idcandidato}
        """
        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        data = pd.read_sql_query(sql_query, self.conn)

        data["apellidopaterno"] = data["apellidopaterno"].apply(lambda texto: texto.strip().title())
        data["apellidomaterno"] = data["apellidomaterno"].apply(lambda texto: texto.strip().title())
        data["nombre"] = data["nombre"].apply(lambda texto: texto.strip().title())
        data["primer_nombre"] = data["nombre"].str.split().str[0]
        data["apellidos_nombres"] = data['apellidopaterno'] + ' ' + data['apellidomaterno'] + ', ' + data['nombre']
        data["file_name"] = data['primer_nombre'] + ' ' + data['apellidopaterno']
        data["estado_civil"] = data["estado_civil"].apply(lambda texto: texto.capitalize())
        data["edad"] = data["fecha_nacimiento"].apply(lambda texto: self.__calcular_edad(texto))

        data.drop(["apellidopaterno", "apellidomaterno", "nombre"], axis=1, inplace=True)

        return data
