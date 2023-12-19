from abc import ABC, abstractmethod


class TestPsicologico(ABC):
    def __init__(self, conn, file_table_comparative: str, idcandidato: int, idtestpsicologico: int):
        self.conn = conn
        self.table_comparative = None
        self.idtestpsicologico = idtestpsicologico
        self.idcandidato = idcandidato
        self.configuracion_test = None
        self.configuracion_preguntas = None
        self.respuestas = None


    # Función para extraer los valores de 'factor' y 'subFactor' de la cadena JSON
    def __extraer_valores(self, row):
        lista = row
        if lista:
            factor = lista[0].get('factor')
            subfactor = lista[0].get('subFactor')
            desviacion = int(lista[0].get('desviacion'))
            return factor, subfactor, desviacion
        return None, None, None


    @abstractmethod
    def get_configuration(self):
        print("Obteniendo configuración ...")


    @abstractmethod
    def get_respuestas_candidate(self):
        pass


    @abstractmethod
    def get_result(self):
        pass


    @abstractmethod
    def get_interpretation(self):
        pass


    @abstractmethod
    def add_data_report(self, data):
        pass


    def __normalize_results(self):
        pass


    def save(self):
        self.__close_conn()


    def __close_conn(self):
        # Cerrar la conexión a la base de datos
        self.conn.close()
