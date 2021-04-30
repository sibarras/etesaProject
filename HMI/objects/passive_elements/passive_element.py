from ..substation_element import SubstationElement, VoltageLevel, Connection

class PassiveElement(SubstationElement):
    def __init__(self, name: str, connection:Connection, position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, position, voltage_level)
        self.connection = connection