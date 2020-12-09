import pandas as pd
import sqlite3
import os
from modules import cells_config

def crear_db_transformador(libro:str, dir_libros:str, dir_dbs:str) -> None:
    plantilla = cells_config.PLANTILLA_TX
    hojas_plantilla = plantilla['hojas']
    nombre_db = libro.rstrip('.xlsx') + '.db'
    dir_db = os.path.join(dir_dbs, nombre_db)

    if nombre_db in os.listdir(dir_dbs):
        try:
            os.remove(dir_db)
            print('Eliminando archivo ({}) y creando nuevo...'.format(libro))
        except Exception as e:
            print('[ERROR]:', e)
            return
    
    conn = sqlite3.connect(dir_db)
    for hoja in hojas_plantilla.values():
        nombre_hoja, fila_titulo = hoja

        dir_libro = os.path.join(dir_libros, libro)
        df = pd.read_excel(dir_libro, nombre_hoja, header=fila_titulo-1)
        print(nombre_hoja)
        print(df)
        
        df.to_sql(nombre_hoja, conn, if_exists='replace')

    conn.close()
    print('Base de datos de {} creada!'.format(libro))

if __name__ == "__main__":
    abs_path = os.path.abspath(__file__).split('\\')
    MAIN_PATH = ''
    for level in abs_path[:-1]:
        MAIN_PATH += level+'/'
    MAIN_PATH = os.path.normpath(MAIN_PATH)
    
    FOLDER_LIBROS = 'cambiar path'
    FOLDER_DB = 'database'
    dir_libros = MAIN_PATH.replace('python', FOLDER_LIBROS)
    dir_dbs = MAIN_PATH.replace('python', FOLDER_DB)

    books = os.listdir(dir_libros)
    for book in books:
        crear_db_transformador(book, dir_libros=dir_libros, dir_dbs=dir_dbs)