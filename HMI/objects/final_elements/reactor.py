from .final_element import FinalElement, VoltageLevel, Connection

class Reactor(FinalElement):
    def __init__(self, name: str, connection: Connection, position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, connection, position, voltage_level)
    
    def specifications(self) -> str:
        return 'Specs in progres...'