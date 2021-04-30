from ..substation_element import SubstationElement, Connection, VoltageLevel

class ConnectionElement(SubstationElement):
    def __init__(self, name: str, connections: dict[SubstationElement, Connection], position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, position, voltage_level)
        self.connections = connections

