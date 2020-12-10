from os import makedirs
from python.data_loader import load_data
from python.db_actualizador import actualizacion_completa
from matplotlib import pyplot as plt


if __name__ == "__main__":
    actualizacion_completa()
