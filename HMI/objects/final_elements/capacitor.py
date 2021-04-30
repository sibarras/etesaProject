from .final_element import FinalElement, VoltageLevel, Connection

class Capacitor(FinalElement):
    def __init__(self, name: str, connection: Connection, position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, connection, position, voltage_level)
    
    def configuration(self) -> str:
        return 'capacitors configuration in process...'