# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from openpyxl import load_workbook
PATH = './Excel Books/'


# %%
#abro el segundo archivo y lo declaro como accounts workbook
accounts_filename = 'accounts_PyM.xlsx'
accounts_wb = load_workbook(PATH + accounts_filename, data_only=True)


# %%
# Abro la hoja de Cuentas de ETESA
accounts_ws = accounts_wb['CUENTAS ETESA']

# Para observar las hojas dentro de un workbook
#accounts_wb.get_sheet_names()

# Otra forma de abrir las hojas
# accounts_ws2 = accounts_wb.get_sheet_by_name('CUENTAS ETESA')


# %%
# Creo mi encabezado para mi lista de cuentas
account_list = []
account_list.append([])
for col in accounts_ws['4:4'][1:]:
    account_list[-1].append(col.value)
print(account_list)


# %%
# Filtrado por el valor de la columna Tipo
coord_index = account_list[0].index('TIPO') + 1
cost_index = account_list[0].index('CENTRO DE COSTO') + 1
for row in accounts_ws.rows:
    if row[coord_index].value == 'MED' and 'PM-MED-' in str(row[cost_index].value):
        account_list.append([])
        for box in row[1:]:
            account_list[-1].append(box.value)

# Para ver los datos de la lista
# for row in account_list:
#     print()
#     for col in row:
#         print(col, end='\t')


# %%
place_data = {}
place_listindex = account_list[0].index('UBICAC')
for place in account_list:
    place_data[place[place_listindex]] = place


# %%
# Otros datos a utilizar
tests = [
    'Tiempos de Operacion',         #0
    'Resistencia de Contacto',      #1
    'Resistencia de Aislamiento',   #2
    'Resistencia de Devanados',     #3
    'Relacion de Vueltas',          #4
    'Factor de Potencia',           #5
    'Analisis de Gas SF6',          #6
    'Analis de Calidad de Energia', #7
    'Corriente de Excitacion',      #8
    'Saturacion'                    #9
    'Alarmas',                      #10
    'Disparos',                     #11
    'Bloqueos',                     #12
    'Tratamiento de gas SF6',       #13 
]
equipmentTests = {
    'PT': [tests[i] for i in [5, 2]],
    'CT': [tests[i] for i in [2, 3, 4, 5, 8, 9]],
    'INT': [tests[i] for i in [0, 1, 6, 10, 12]],
    'TX': [tests[i] for i in [5, 8, 4, 3, 10, 11]],
    'RX': [tests[i] for i in [5, 10, 11]]
}


# %%
# Abro el primer archivo y lo declaro como payroll workbook
payroll_filename = 'payroll_layout.xlsx'
payroll_wb = load_workbook(PATH + payroll_filename)


# %%
# Para la distribucion del tiempo
distribution_ws = payroll_wb['DISTRIBUCION']

# Para las horas extras
extra_ws = payroll_wb['EXTRAS']


# %%



