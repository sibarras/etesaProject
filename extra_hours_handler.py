from excel_handler import ExcelHandler
from datetime import datetime, date
import calendar
import programData

class ExtraHours(ExcelHandler):
    def __init__(self, month=date.today().month, half=(1 if date.today().day<16 else 2), layout_filename='./Excel Books/payroll_layout'):
        super().__init__(f'{layout_filename}.xlsx')
        
        self.loadWorksheet('EXTRAS')
        self.__load_cells_data()

        self.month = month
        self.half = half

    def __load_cells_data(self):
        self.nombre_cell = 'I11'
        self.cedula_cells = [f'{chr(i)}9' for i in range(ord('T'), ord('Z')+1)]\
                + [f'A{chr(i)}9' for i in range(ord('A'), ord('D')+1)]
        self.numEmpleado_cell = 'X11'
        self.gerencia_cell = 'I12'
        self.depto_cell = 'Z12'
        self.cargo_cell = 'I13'
        self.periodo_cells = ['X13','AB13']

        lugar_rows = [str(col) for col in range(17, 21+1)]
        dias_cols = [f'{chr(i)}' for i in range(ord('R'), ord('Z')+1)]\
                    + [f'A{chr(i)}' for i in range(ord('A'), ord('G')+1)]
        self.lugar_cells = lambda col, row: f'{dias_cols[col]}{lugar_rows[row]}'
        
        codigoLugar_col = 'C'
        self.codigoLugar_cells = [f'{codigoLugar_col}{lugar_row}' for lugar_row in lugar_rows]

        tarea_rows = [str(col) for col in range(25, 33+1)]
        tarea_col = 'C'
        self.tarea_cells = [f'{tarea_col}{tarea_row}' for tarea_row in tarea_rows]

        rangoHoras_cols = ['AB','AF']
        self.horaInicial_cells = [f'{rangoHoras_cols[0]}{tarea_row}' for tarea_row in tarea_rows]
        self.horaFinal_cells = [f'{rangoHoras_cols[1]}{tarea_row}' for tarea_row in tarea_rows]

        self.enfermedad_cells = [f'{dias_col}37' for dias_col in dias_cols]
        self.fiestaDuelo_cells = [f'{dias_col}38' for dias_col in dias_cols]
        self.accidente_cells = [f'{dias_col}39' for dias_col in dias_cols]
        self.adiestram_cells = [f'{dias_col}40' for dias_col in dias_cols]
        self.vacaciones_cells = [f'{dias_col}41' for dias_col in dias_cols]
        self.compensatiorio_cells = [f'{dias_col}42' for dias_col in dias_cols]
        self.sindical_cells = [f'{dias_col}43' for dias_col in dias_cols]
        self.otros_cells = [f'{dias_col}44' for dias_col in dias_cols]

    def write_personal_data(self, personal_data:dict):
        # Ahora introducir estos datos en el extra worksheet
        self.ws[self.nombre_cell] = personal_data['nombre'].upper()
        self.ws[self.numEmpleado_cell] = personal_data['num_empleado']
        self.ws[self.gerencia_cell] = personal_data['gerencia'].upper()
        self.ws[self.depto_cell] = personal_data['depto'].upper()
        self.ws[self.cargo_cell] = personal_data['cargo'].upper()

        # cedula
        ced_parts = personal_data['cedula'].split('-')
        ced_slots = ([1,5,5] if len(ced_parts)== 3 else [1,2,3,5])
        for cell in self.cedula_cells:
            self.ws[cell] = 0

        # aplicar
        for part in reversed(ced_parts):
            for num in reversed(part):
                self.ws[self.cedula_cells[-1]] = num
                self.cedula_cells.pop()
            while len(self.cedula_cells) > sum(ced_slots[:-1]):
                self.cedula_cells.pop()
            ced_slots.pop()

    def write_time_data(self, spanishDict=programData.spanishDict):

        self.year = date.today().year
        self.nombre_mes = programData.spanishDict[calendar.month_name[self.month]]
        self.nombre_dia = lambda d: programData.spanishDict[calendar.day_name[calendar.weekday(self.year, self.month, d)]]
        self.dia_fin_mes = calendar._monthlen(self.year, self.month)

        periodo_planilla = lambda : 1 if self.half == 1 else 16,\
                           lambda : f'15 de {self.nombre_mes}' if self.half == 1\
                                    else f'{self.dia_fin_mes} de {self.nombre_mes}' 

        # aplico datos en worksheet
        self.ws[self.periodo_cells[0]] = periodo_planilla[0]()
        self.ws[self.periodo_cells[1]] = periodo_planilla[1]().upper()

    def write_works(self, works:dict, accounts_data:dict):
        self.works = works
        self.__data_validation()
        self.__write_codes_and_days(accounts_data)
        self.__make_justifications(programData.equipmentGeneralTest, programData.nombres_generales, programData.nombre_SE)
        self.__write_justification_and_hours()

    def __data_validation(self):

        if self.half not in [1,2]:
            print('ERROR EN VALORES INTRODUCIDOS PARA DETERMINAR CUAL ES LA QUINCENA')
            exit()
        self.works_count = 0

        for data in self.works.values():
            if self.works_count == 0:
                self.works_count = len(data)
            if len(data) != self.works_count:
                print('ERROR EN CANTIDAD DE DATOS EN LOS TRABAJOS')
                exit()

        for day in self.works['day']:
            if 1 > day or day > 15 and self.half == 1 or self.dia_fin_mes < day or day < 15 and self.half == 2:
                print('ERROR EN DIA ESTIPULADO POR ESTAR FUERA DEL PERIODO')
                exit()

    def __write_codes_and_days(self, accounts_data:dict):
        codes_in_ws = []  # Registro de Lugares ya escritos

        end_num = lambda end: int(end.split(':')[0]) + int(end.split(':')[1])/60
        init_num = lambda init: int(init.split(':')[0]) + int(init.split(':')[1])/60

        horas_trabajo = lambda init, end : ((int((end_num(end) - init_num(init))*100))/100\
             if end_num(end)-init_num(init)>0 else (int((12 + end_num(end) - init_num(end))*100))/100)

        for n in range(self.works_count):
            # Se toma de la base de datos
            current_code = accounts_data.loc[accounts_data['UBICAC']==self.works['place'][n]]['CUENTA CONTABLE'].values[0]

            # Codigos
            if current_code not in codes_in_ws:
                self.ws[self.codigoLugar_cells[n]] = current_code
                codes_in_ws.append(current_code)

            # horas en dias
            code_index = codes_in_ws.index(current_code)
            self.ws[self.lugar_cells(self.works['day'][n]-(1 if self.half==1 else 16), code_index)]\
                                    = horas_trabajo(self.works['init'][n], self.works['end'][n])

    def __make_justifications(self, equipmentTests, nombres_generales, nombre_SE): # USA LOS VALORES DE LOS TEST PARA REALIZAR SU TRABAJO

        self.justification_char = []
        for n in range(self.works_count):
            pruebas = ''
            testList = equipmentTests[self.works['equip'][n]]
            if len(testList) == 1:  # Determina si solo hay 1 prueba
                pruebas = testList[0]
            else:  # Si hay varias pruebas
                for test in testList:
                    if test == testList[-1]:  # En caso de ser la ultima prueba
                        pruebas = pruebas[:-2] + ' y ' + test
                        continue
                    pruebas += test + ', '

            nombre_equipo = nombres_generales[self.works['equip'][n]] +' ' + self.works["name"][n]

            just_n = '{} {} de {} de {}: {} al {} en {}'.format(
                self.nombre_dia(self.works["day"][n]), self.works["day"][n], self.nombre_mes,\
                self.year, pruebas, nombre_equipo, nombre_SE[self.works["place"][n]])
            
            self.justification_char.append(just_n)

    def __write_justification_and_hours(self):
        for n in range(self.works_count):
            self.ws[self.tarea_cells[n]] = self.justification_char[n]

            init_h, init_m = self.works['init'][n].split(':')
            end_h, end_m = self.works['end'][n].split(':')
            init_suffix = (' a.m.' if int(init_h)<12 else ' p.m.')
            end_suffix = (' a.m.' if int(end_h)<12 else ' p.m.')

            init = (self.works['init'][n]+init_suffix if int(init_h)<=12 \
                else '{}:{}{}'.format(int(init_h)-12, init_m, init_suffix))
            end = (self.works['end'][n]+end_suffix if int(end_h)<=12 \
                else '{}:{}{}'.format(int(end_h)-12, end_m, end_suffix))

            self.ws[self.horaInicial_cells[n]] = init
            self.ws[self.horaFinal_cells[n]] = end

    def write_non_worked_days(self):
            print('horas no laboradas en desarrollo')

    def save_document(self, output_filename=str):

        PATH = './Excel Books/results/'
        if len(output_filename) == 0:
            output_filename = 'Planilla {} 15na de {} de {}'.format(('1ra' if self.half==1 else '2da'), self.nombre_mes, self.year)
        self.wb.save(PATH + '{}.xlsx'.format(output_filename))

# PARA PRUEBA
if __name__ == '__main__':
    import pandas as pd
    import sqlite3
    
    personal_data = {
    'nombre': 'Samuel Eliezer Ibarra Solis',
    'cedula': '8-892-2460',
    'num_empleado': '27720',
    'gerencia': 'Proteccion y Comunicacion',
    'depto': 'Pruebas y Mediciones',
    'cargo': 'Especialista en Pruebas y Mediciones'
    }

    works = {
    'place':['SPANAMA', 'SPANAMA2', 'SPANAMA'],
    'day':[23, 26, 30],
    'init':['3:30', '6:00', '3:30'],
    'end':['6:45', '7:00', '4:30'],
    'equip':['CT', 'TX', 'PT']
    }

    db_name = './database/accounts.db'
    conn = sqlite3.connect(db_name)
    accounts_data = pd.read_sql_query('SELECT * FROM accounts', conn)
    conn.close()

    wb = ExtraHours(11,2)
    wb.write_personal_data(personal_data)
    wb.write_time_data()
    wb.write_works(works, accounts_data)
    wb.write_non_worked_days()

    wb.save_document()