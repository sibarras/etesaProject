import pandas as pd
import sqlite3, os
from pathlib import Path
from python import cells_config

def crear_db_transformador(libro:str, dir_dbs:str, overwrite=True) -> None:
    plantilla = cells_config.tipo['Transformador']
    hojas_plantilla = plantilla['hojas']
    dir_libro = Path(libro)
    excel_data_path = [dir_libro.parents[i] for i in range(len(dir_libro.parts)-1)\
                     if dir_libro.parents[i].name=='Historial de Pruebas'][0]
    rdir_libro = dir_libro.parent.relative_to(excel_data_path)
    nombre_db = dir_dbs / rdir_libro.parent / (rdir_libro.name + '.db')
    print(rdir_libro.name)
    if nombre_db.is_file():
        if overwrite:
            print('Eliminando archivo ({}) y creando nuevo...'.format(str(nombre_db)))
        else:
            print('No se realizó ninguna modificación')
            return

    else:
        os.makedirs(str(nombre_db.parent), exist_ok=True)
    
    conn = sqlite3.connect(str(nombre_db))
    for hoja in hojas_plantilla.values():
        nombre_hoja, fila_titulo = hoja
        try:
            df = pd.read_excel(libro, nombre_hoja, header=fila_titulo-1)
            df.to_sql(nombre_hoja, conn, if_exists='replace')
        except Exception as e:
            print('[ERROR Leyendo o escribiendo la base de datos]:', e)

    conn.close()
    print('Base de datos de {} creada!'.format(libro))

def actualizacion_completa() -> None:
    p = Path(__file__).parents[2]
    database_path = p/'app'/'database'
    excel_list = [str(excel) for excel in p.glob('**/*.xls*')]
    if database_path.is_dir():
        for excel_name in excel_list:
            crear_db_transformador(libro=excel_name, dir_dbs=database_path)