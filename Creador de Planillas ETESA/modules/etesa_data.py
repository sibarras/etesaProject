import pandas as pd
import sqlite3
import os

db_folder=__file__.rstrip('/etesa_data.py').rstrip('/modules') + '/database'
db_folder = os.path.normpath(db_folder)
db_dir = os.listdir(db_folder)
verification = 'colaborators.db'not in db_dir and __name__ == '__main__'

if verification:
    colaborators_dict = {0:{
    'nombre': 'Samuel Eliezer Ibarra Solis',
    'cedula': '8-892-2460',
    'num_empleado': '27720',
    'gerencia': 'Protección y Comunicación',
    'depto': 'Pruebas y Mediciones',
    'cargo': 'Especialista en Pruebas y Mediciones'
    },
    1:{
    'nombre': 'Paola Yanabel Solís',
    'cedula': '6-717-537',
    'num_empleado': '27829',
    'gerencia': 'Protección y Comunicación',
    'depto': 'Pruebas y Mediciones',
    'cargo': 'Especialista en Pruebas y Mediciones'
    },
    2:{
    'nombre': 'Mónica Itzel Pérez',
    'cedula': '8-756-1579',
    'num_empleado': '27819',
    'gerencia': 'Protección y Comunicación',
    'depto': 'Pruebas y Mediciones',
    'cargo': 'Especialista en Pruebas y Mediciones'
    }
    }
    formatted_dict = {}
    for num, dct in colaborators_dict.items():
        for category, info in dct.items():
            if category not in formatted_dict.keys():
                formatted_dict[category] = {}
            formatted_dict[category][num] = info
    colaborators = pd.DataFrame(formatted_dict)

    conn = sqlite3.connect(db_folder+'/colaborators.db')
    colaborators.to_sql('colaborators', conn)
    conn.close()
else:
    conn = sqlite3.connect(db_folder+'/colaborators.db')
  
    res = pd.read_sql_query('SELECT * FROM colaborators', conn, index_col='index', )
    conn.close()

    print(res['nombre'].tolist())