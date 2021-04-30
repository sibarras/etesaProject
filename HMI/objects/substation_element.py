from typing import Any
from .extra.voltage_level import VoltageLevel
from .extra.connection import Connection

class SubstationElement:
    def __init__(self, name:str, position:tuple[int,int], voltage_level:VoltageLevel) -> None:
        self.name = name.upper()
        self.voltage_level = voltage_level
        self.position = position
        self.rgb_color = self.voltage_level.rgb_color
        self.figure = None

    def draw_element(self, window) -> Any:
        return Any


    
