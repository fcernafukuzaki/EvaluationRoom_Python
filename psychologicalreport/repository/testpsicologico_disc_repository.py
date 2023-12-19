import pandas as pd
from psychologicalreport.repository.testpsicologico_repository import TestPsicologico


class TestPsicologicoDISC(TestPsicologico):
    def __init__(self, conn, file_table_comparative: str, idcandidato: int, idtestpsicologico=3):
        super().__init__(conn, file_table_comparative, idcandidato, idtestpsicologico)
        self.table_comparative = pd.read_excel(file_table_comparative, header=3)


    # Función para extraer los valores de 'factor' y 'subFactor' de la cadena JSON
    # def __extraer_valores(self, row):
    #     # lista = row#json.loads(row)
    #     # if lista:
    #     #     factor = lista[0].get('factor')
    #     #     subfactor = lista[0].get('subFactor')
    #     #     desviacion = int(lista[0].get('desviacion'))
    #     #     return factor, subfactor, desviacion
    #     return None, None, None


    def get_configuration(self):
        # sql_query = f"""
        # SELECT idparte, idpregunta, configuracion
        # FROM evaluationroom.testpsicologicointerpretacion
        # WHERE idtestpsicologico={self.idtestpsicologico}
        # ORDER BY idtestpsicologico DESC, idparte ASC, idpregunta ASC
        # """
        # # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        # config = pd.read_sql_query(sql_query, self.conn)

        # config['configuracion'] = config['configuracion'].apply(str)
        # config['configuracion'] = config['configuracion'].apply(ast.literal_eval)
        # # Crear las columnas nuevas
        # config[['factor', 'subFactor', 'desviacion']] = config['configuracion'].apply(lambda x: pd.Series(self._TestPsicologico__extraer_valores(x)))
        # config.drop('configuracion', axis=1, inplace=True)

        # self.configuracion_test = config[config["idpregunta"] == 0]
        # self.configuracion_preguntas = config[config["idpregunta"] != 0]
        pass


    def get_respuestas_candidate(self):
        pass


    def get_result(self):
        pass


    def get_interpretation(self):
        sql_query = f"""
        SELECT resultado
        FROM evaluationroom.candidatotest
        WHERE idtestpsicologico={self.idtestpsicologico}
        AND idcandidato={self.idcandidato}
        ORDER BY idcandidato DESC
        """
        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        resultado = pd.read_sql_query(sql_query, self.conn)

        resultados_disc = resultado["resultado"][0]

        puntaje_D = int([puntaje['resultado'] for puntaje in resultados_disc['puntajes'] if puntaje['factor'] == 'D'][0])
        puntaje_I = int([puntaje['resultado'] for puntaje in resultados_disc['puntajes'] if puntaje['factor'] == 'I'][0])
        puntaje_S = int([puntaje['resultado'] for puntaje in resultados_disc['puntajes'] if puntaje['factor'] == 'S'][0])
        puntaje_C = int([puntaje['resultado'] for puntaje in resultados_disc['puntajes'] if puntaje['factor'] == 'C'][0])

        fortalezas_D = str([puntaje['resultado'] for puntaje in resultados_disc['fortalezas'] if puntaje['factor'] == 'D'][0]).capitalize()
        fortalezas_I = str([puntaje['resultado'] for puntaje in resultados_disc['fortalezas'] if puntaje['factor'] == 'I'][0]).capitalize()
        fortalezas_S = str([puntaje['resultado'] for puntaje in resultados_disc['fortalezas'] if puntaje['factor'] == 'S'][0]).capitalize()
        fortalezas_C = str([puntaje['resultado'] for puntaje in resultados_disc['fortalezas'] if puntaje['factor'] == 'C'][0]).capitalize()

        debilidades_D = str([puntaje['resultado'] for puntaje in resultados_disc['debilidades'] if puntaje['factor'] == 'D'][0]).capitalize()
        debilidades_I = str([puntaje['resultado'] for puntaje in resultados_disc['debilidades'] if puntaje['factor'] == 'I'][0]).capitalize()
        debilidades_S = str([puntaje['resultado'] for puntaje in resultados_disc['debilidades'] if puntaje['factor'] == 'S'][0]).capitalize()
        debilidades_C = str([puntaje['resultado'] for puntaje in resultados_disc['debilidades'] if puntaje['factor'] == 'C'][0]).capitalize()

        result = {
            "D": {
                "puntaje": puntaje_D,
                "fortalezas": fortalezas_D,
                "debilidades": debilidades_D
            },
            "I": {
                "puntaje": puntaje_I,
                "fortalezas": fortalezas_I,
                "debilidades": debilidades_I
            },
            "S": {
                "puntaje": puntaje_S,
                "fortalezas": fortalezas_S,
                "debilidades": debilidades_S
            },
            "C": {
                "puntaje": puntaje_C,
                "fortalezas": fortalezas_C,
                "debilidades": debilidades_C
            }
        }

        return result


    def add_data_report(self, data):
        result = self.get_interpretation()
        data["puntaje_D"] = result["D"]["puntaje"]
        data["fortalezas_D"] = result["D"]["fortalezas"]
        data["debilidades_D"] = result["D"]["debilidades"]
        data["puntaje_I"] = result["I"]["puntaje"]
        data["fortalezas_I"] = result["I"]["fortalezas"]
        data["debilidades_I"] = result["I"]["debilidades"]
        data["puntaje_S"] = result["S"]["puntaje"]
        data["fortalezas_S"] = result["S"]["fortalezas"]
        data["debilidades_S"] = result["S"]["debilidades"]
        data["puntaje_C"] = result["C"]["puntaje"]
        data["fortalezas_C"] = result["C"]["fortalezas"]
        data["debilidades_C"] = result["C"]["debilidades"]
        return data