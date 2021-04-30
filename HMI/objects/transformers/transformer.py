from ..substation_element import SubstationElement, VoltageLevel, Connection

class Transformer(SubstationElement):
    def __init__(self, name: str, connection: dict[VoltageLevel, Connection], position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, position, voltage_level)
        self.connection = connection