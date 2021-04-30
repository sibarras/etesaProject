from .voltage_level import VoltageLevel

class Connection:
    def __init__(self, coordinates:tuple[int, int] = (-1, -1)):
        self.coordinates = coordinates
