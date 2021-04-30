from .flux_element import FluxElement, Connection, VoltageLevel

class Breaker(FluxElement):
    def __init__(self, name: str, init_conn: Connection, final_conn: Connection, position: tuple[int, int], voltage_level: VoltageLevel) -> None:
        super().__init__(name, init_conn, final_conn, position, voltage_level)
