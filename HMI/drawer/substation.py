from objects.extra.connection import Connection
from objects.extra.voltage_level import VoltageLevel
from objects.substation_element import SubstationElement
import cv2
import numpy as np

class SubstationWindow:
    def __init__(self, name:str, window_size: tuple[int, int] = (512,512)) -> None:
        self.name = name
        self.window = np.zeros((*window_size, 3), np.uint8)
        self.window_active:bool = False
    
    def show(self, delay_ms:int = 0, close_with_key:bool = False) -> None:
        cv2.imshow(self.name, self.window)
        self.window_active = True 
        self.__window_wait(delay_ms, close_with_key)
    
    def __window_wait(self, delay_ms:int = 0, close_with_key:bool = False) -> None:
        assert self.window_active
        if delay_ms == 0: delay_ms = 1
        if close_with_key:
            cv2.waitKey(0)
            return None
        else:
            cv2.waitKey(delay_ms)

    def close_windows(self) -> None:
        assert self.window_active
        cv2.destroyAllWindows()
        self.window_active = False
    
    def draw_line(self, init_conn:Connection, final_conn:Connection, voltage_level:VoltageLevel, delay_ms:int = 0, close_with_key:bool = False) -> None:
        self.window = cv2.line(self.window, init_conn.coordinates, final_conn.coordinates, voltage_level.rgb_color)
        self.show(delay_ms, close_with_key)
    
    def draw_substation_element(self, substation_element:SubstationElement, delay_ms:int = 0, close_with_key:bool = False) -> None:
        
        self.window = substation_element.draw_element(self.window)