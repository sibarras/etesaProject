# Organize

rgb_dict = {
    'Magenta': (229, 9, 127), 
    'Cyan': (0, 255, 255),
    'Yellow': (255, 233, 0),
}

color_dict = {
    230: 'Magenta',
    115: 'Cyan',
    34: 'Yellow',
}

class VoltageLevel:
    def __init__(self, level:int) -> None:
        self.level:int = level
        self.color_name:str = color_dict[self.level]
        self.rgb_color:tuple[int,int,int] = rgb_dict[self.color_name]
