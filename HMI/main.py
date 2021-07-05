import drawer
from sys import path
from pathlib import Path
path.append(Path(__file__).parent.__str__())

from drawer.substation import SubstationWindow
from objects.extra.connection import Connection
from objects.extra.voltage_level import VoltageLevel

if __name__ == "__main__":
    from time import sleep

    init = Connection((2,9))
    end = Connection((511,511))
    vtg = VoltageLevel(level=230)

    sub = SubstationWindow('Panama', window_size=(512, 512))
    sub.show(delay_ms=1000)
    sub.draw_line(init, end, vtg, close_with_key=True)
    sub.close_windows()
