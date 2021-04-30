from ..substation_element import SubstationElement, Connection, VoltageLevel

# Elements that have continuity and two connections
class FluxElement(SubstationElement):
    def __init__(self, name:str, init_conn:Connection, final_conn:Connection, position:tuple[int,int], voltage_level:VoltageLevel) -> None:
        super().__init__(name, position, voltage_level)
        self.init_conn = init_conn
        self.final_conn = final_conn

