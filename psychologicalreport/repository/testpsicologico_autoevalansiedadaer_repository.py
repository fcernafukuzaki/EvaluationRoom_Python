import ast
import pandas as pd
from psychologicalreport.repository.testpsicologico_repository import TestPsicologico


class TestPsicologicoAutoevalAnsiedadAER(TestPsicologico):
    def __init__(self, conn, file_table_comparative: str, gender: bool, idcandidato: int, idtestpsicologico=7):
        super().__init__(conn, file_table_comparative, idcandidato, idtestpsicologico)
        self.table_comparative = pd.read_excel(file_table_comparative, header=3)
        self.gender = gender


    def get_configuration(self):
        sql_query = f"""
        SELECT idparte, idpregunta, configuracion
        FROM evaluationroom.testpsicologicointerpretacion
        WHERE idtestpsicologico={self.idtestpsicologico}
        ORDER BY idtestpsicologico DESC, idparte ASC, idpregunta ASC
        """
        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        config = pd.read_sql_query(sql_query, self.conn)

        config['configuracion'] = config['configuracion'].apply(str)
        config['configuracion'] = config['configuracion'].apply(ast.literal_eval)
        # Crear las columnas nuevas
        config[['factor', 'subFactor', 'desviacion']] = config['configuracion'].apply(lambda x: pd.Series(self._TestPsicologico__extraer_valores(x)))
        config.drop('configuracion', axis=1, inplace=True)

        self.configuracion_test = config[config["idpregunta"] == 0]
        self.configuracion_preguntas = config[config["idpregunta"] != 0]


    def get_respuestas_candidate(self):
        # Definir la consulta SQL
        sql_query = f"""
        SELECT idparte, idpregunta, respuesta
        FROM evaluationroom.candidatotestdetalle
        WHERE idtestpsicologico={self.idtestpsicologico} AND idcandidato={self.idcandidato}
        ORDER BY idtestpsicologico DESC, idparte ASC, idpregunta ASC
        """

        # Ejecutar la consulta SQL y obtener los resultados en un dataframe
        self.respuestas = pd.read_sql_query(sql_query, self.conn)

        if self.respuestas.empty:
            print("El candidato no tiene respuestas.")
        self.__normalize_results()
        return self.respuestas


    def get_result(self):
        self.get_respuestas_candidate()

        if self.respuestas.empty:
            return None, None

        self.get_configuration()

        df_merged = pd.merge(self.respuestas, self.configuracion_preguntas, on=['idparte','idpregunta'], how='inner')
        df_merged['resultado_temp'] = df_merged['respuesta'] * df_merged['desviacion']
        df_grouped = df_merged.groupby(['factor','idparte']).agg({'resultado_temp': 'sum'}).reset_index()
        df_grouped = pd.merge(df_grouped, self.configuracion_test, on=['factor','idparte'], how='inner')
        df_grouped['resultado_temp'] = df_grouped['resultado_temp'] + df_grouped["desviacion"]

        df_result = df_grouped.copy()

        resultado_estado = int(df_result["resultado_temp"].values[0])
        resultado_rasgo = int(df_result["resultado_temp"].values[1])
        return resultado_estado, resultado_rasgo


    def get_interpretation(self):
        resultado_estado, resultado_rasgo = self.get_result()

        if resultado_estado is None or resultado_rasgo is None:
            return None

        df = self.table_comparative

        flag_gender = "VARONES" if self.gender else "MUJERES"
        columnas = ["CATEGORIAS",
                    f"{flag_gender} A/E MIN",
                    f"{flag_gender} A/E MAX",
                    f"{flag_gender} A/R MIN",
                    f"{flag_gender} A/R MAX"]

        categoria_estado = str(df[columnas][
            (df[f"{flag_gender} A/E MIN"] <= resultado_estado) & (resultado_estado <= df[f"{flag_gender} A/E MAX"])
            ]["CATEGORIAS"].values[0])
        categoria_rasgo = str(df[columnas][
            (df[f"{flag_gender} A/R MIN"] <= resultado_rasgo) & (resultado_rasgo <= df[f"{flag_gender} A/R MAX"])
            ]["CATEGORIAS"].values[0])

        result = {
            "estado": {
                "resultado": resultado_estado,
                "categoria": categoria_estado
            },
            "rasgo": {
                "resultado": resultado_rasgo,
                "categoria": categoria_rasgo
            }
        }

        return result


    def add_data_report(self, data):
        result = self.get_interpretation()
        data["resultado_ansiedad_estado"] = result["estado"]["categoria"]
        data["resultado_ansiedad_rasgo"] = result["rasgo"]["categoria"]
        return data


    def __normalize_results(self):
        self.respuestas['respuesta'] = self.respuestas['respuesta'].apply(str)
        self.respuestas['respuesta'] = self.respuestas['respuesta'].apply(ast.literal_eval)
        self.respuestas['respuesta'] = self.respuestas['respuesta'].apply(lambda x: int(x[0]['respuesta']))
