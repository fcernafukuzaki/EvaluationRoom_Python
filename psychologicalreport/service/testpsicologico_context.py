# Define the Context class that will use the Strategy pattern
from psychologicalreport.repository.testpsicologico_repository import TestPsicologico


class TestPsicologicoContext:
    """
    The Context defines the interface of interest to clients.
    """

    def __init__(self, testpsicologico: TestPsicologico) -> None:
        self._strategy = testpsicologico


    @property
    def strategy(self) -> TestPsicologico:
        """
        The Context maintains a reference to one of the Strategy objects. The
        Context does not know the concrete class of a strategy. It should work
        with all strategies via the Strategy interface.
        """

        return self._strategy


    @strategy.setter
    def strategy(self, testpsicologico: TestPsicologico) -> None:
        """
        The Context allows replacing a Strategy object at runtime.
        """

        self._strategy = testpsicologico


    def get_interpretation(self):
        return self._strategy.get_interpretation()


    def add_data_report(self, data):
        return self._strategy.add_data_report(data)