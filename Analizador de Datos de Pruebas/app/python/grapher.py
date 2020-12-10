from matplotlib import pyplot as plt
import pandas as pd
from python.data_loader import load_data

class Grapher:
    def __init__(self, db_name:str) -> None:
        load_data(db_name=db_name)

    def draw_graph(self, x_axis:list, y_axis:list, title:str, params:dict):
        plt.plot(x_axis, y_axis)



