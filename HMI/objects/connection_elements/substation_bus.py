from .connection_element import ConnectionElement, SubstationElement, VoltageLevel, Connection

class Bus(ConnectionElement):
    def __init__(self, name: str, connections: dict[SubstationElement, Connection], position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, connections, position, voltage_level)