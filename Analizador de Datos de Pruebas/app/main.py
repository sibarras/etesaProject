# from sys import path
# from pathlib import Path
# modules_folder = 'python'
# modules_path = Path(__file__).parent / modules_folder
# path.append(str(modules_path))

from python.data_loader import load_data
from python.db_actualizador import actualizacion_completa
from matplotlib import pyplot as plt


if __name__ == "__main__":
    actualizacion_completa()
