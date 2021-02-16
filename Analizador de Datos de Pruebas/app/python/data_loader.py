import pandas as pd
import sqlite3
import os
from python import cells_config

def load_data(db_name:str, type:str) -> dict:

    PLANTILLA_TX = cells_config.tipo['Transformador']
    db_dir = os.path.normpath(db_name)
    df_dict = {}
    conn = sqlite3.connect(db_dir)
    try:
        for hoja in PLANTILLA_TX['hojas'].values():
            tabla = hoja[0]
            df = pd.read_sql_query("SELECT * FROM [{}]".format(tabla), conn)
            df_dict[tabla] = df
    except Exception as e:
        print(f'[ERROR GETTING DATA FROM DB ON {__name__}]:', e)
        df_dict = None
    finally:
        conn.close()
    return df_dict


if __name__ == "__main__" and False:
    abs_path = os.path.abspath(__file__).split('\\')
    MAIN_PATH = ''
    for level in abs_path[:-1]:
        MAIN_PATH += level+'/'
    MAIN_PATH = os.path.normpath(MAIN_PATH)

    db_path = MAIN_PATH.replace('python', 'database')
    db_names = os.listdir(db_path)
    db_name = db_names[0]
    db_name = os.path.join(db_path, db_name)
    
    df_dict = load_data(db_name)
    print(df_dict.keys())
    for df in df_dict.values():
        print(df)