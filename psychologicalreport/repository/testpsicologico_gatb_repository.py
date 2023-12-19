import pandas as pd
from psychologicalreport.repository.testpsicologico_repository import TestPsicologico


class TestPsicologicoGATB(TestPsicologico):
    def __init__(self, conn, file_table_comparative: str, idcandidato: int, idtestpsicologico=2):
        super().__init__(conn, file_table_comparative, idcandidato, idtestpsicologico)
        self.table_comparative = pd.read_excel(file_table_comparative, header=3)


    def get_configuration(self):
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
        resultados = pd.read_sql_query(sql_query, self.conn)
        resultados = resultados["resultado"][0]
        result = dict()
        for resultado in resultados:
            result[resultado['factor']] = {'factor': resultado['factor'],
                                            'resultado': resultado['resultado'],
                                            'interpretacion': resultado['interpretacion']}

        return result


    def add_data_report(self, data):
        result = self.get_interpretation()
        data["resultado_gatb_general"] = result["Promedio General"]["interpretacion"]
        return data