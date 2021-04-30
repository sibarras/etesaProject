from .passive_element import PassiveElement, VoltageLevel, Connection

class CurrentTransformer(PassiveElement):
    def __init__(self, name: str, connection: Connection, position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, connection, position, voltage_level)
        