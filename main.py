from extra_hours_handler import ExtraHours
import distribution_handler
import pandas as pd
import sqlite3

personal_data = {
'nombre': 'Samuel Eliezer Ibarra Solis',
'cedula': '8-892-2460',
'num_empleado': '27720',
'gerencia': 'Protección y Comunicación',
'depto': 'Pruebas y Mediciones',
'cargo': 'Especialista en Pruebas y Mediciones'
}

works = {
'place':['SPANAMA', 'SPANAMA2', 'SPANAMA'],
'day':[23, 26, 30],
'init':['3:30', '6:00', '3:30'],
'end':['6:45', '7:00', '4:30'],
'equip':['CT', 'TX', 'PT'],
'name':['11A3', 'T-3', 'PT-34']
}

db_name = './database/accounts.db'
conn = sqlite3.connect(db_name)
accounts_data = pd.read_sql_query('SELECT * FROM accounts', conn)
accounts_data_dict = accounts_data.to_dict()
conn.close()

wb = ExtraHours(11,2)
wb.write_personal_data(personal_data)
wb.write_time_data()
wb.write_works(works, accounts_data)
wb.write_non_worked_days()

wb.save_document()
