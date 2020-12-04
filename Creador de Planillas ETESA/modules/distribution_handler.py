from modules.excel_handler import ExcelHandler
from modules.program_data import nombre_SE_corto
import modules.extra_hours_handler

class Distribution(modules.extra_hours_handler.ExtraHours):
    def __init__(self, month:str, half:str, layout_filename:str):
        ExcelHandler.__init__(self, f'{layout_filename}.xlsx')
        self.loadWorksheet('DISTRIBUCION')
        self.__load_cells_data()

        self.month = month
        self.half = half
    
    def __load_cells_data(self):
        self.nombre_cell = 'F7'
        self.cedula_cells = [f'{chr(i)}6' for i in range(ord('S'), ord('Z')+1)]\
                    + [f'A{chr(i)}6' for i in range(ord('A'), ord('C')+1)]
        self.numEmpleado_cell = 'W7'
        self.gerencia_cell = 'F8'
        self.depto_cell = 'W8'
        self.cargo_cell = 'F9'
        self.periodo_cells = ['Y9','AB9']

        codigo_norm_rows = [str(x*4+13) for x in range(13)]
        nombre_extra_rows = [str(x*4+14) for x in range(13)]

        lugar_col = 'B'
        self.nombreLugar_cells = [f'{lugar_col}{nombre_row}' for nombre_row in nombre_extra_rows]
        self.codigoLugar_cells = [f'{lugar_col}{codigo_row}' for codigo_row in codigo_norm_rows]

        dias_cols = [f'{chr(i)}' for i in range(ord('Q'), ord('Z')+1)]\
                + [f'A{chr(i)}' for i in range(ord('A'), ord('F')+1)]
        self.horas_norm_cells = lambda col, row: f'{dias_cols[col]}{codigo_norm_rows[row]}'
        self.horas_extra_cells = lambda col, row: f'{dias_cols[col]}{nombre_extra_rows[row]}'

        self.enfermedad_cells = [f'{dias_col}69' for dias_col in dias_cols]
        self.fiestaDuelo_cells = [f'{dias_col}70' for dias_col in dias_cols]
        self.accidente_cells = [f'{dias_col}71' for dias_col in dias_cols]
        self.adiestram_cells = [f'{dias_col}72' for dias_col in dias_cols]
        self.vacaciones_cells = [f'{dias_col}73' for dias_col in dias_cols]
        self.compensatiorio_cells = [f'{dias_col}74' for dias_col in dias_cols]
        self.sindical_cells = [f'{dias_col}75' for dias_col in dias_cols]
        self.otros_cells = [f'{dias_col}76' for dias_col in dias_cols]

        self.dias_cols = dias_cols

    def write_works(self, works:dict, accounts_data:dict):
        self.works = works
        self._data_validation()
        self.__write_codes_and_extra_days(accounts_data, nombre_SE_corto)

    def __write_codes_and_extra_days(self, accounts_data:dict, SE_names:dict):
        codes_in_ws = []  # Registro de Lugares ya escritos

        end_num = lambda end: int(end.split(':')[0]) + int(end.split(':')[1])/60
        init_num = lambda init: int(init.split(':')[0]) + int(init.split(':')[1])/60

        horas_trabajo = lambda init, end: ((int((end_num(end) - init_num(init))*100))/100\
             if end_num(end)-init_num(init)>0 else (int((12 + end_num(end) - init_num(end))*100))/100)

        for n in range(self.works_count):
            # Se toma de la base de datos el nombre y el codigo
            current_name = self.works['place'][n]
            current_code = accounts_data.loc[accounts_data['UBICAC']==current_name]['CUENTA CONTABLE'].values[0]

            # Codigos y Nombres - se le suma 1 para evitar anadir en la fila de base.
            if current_code not in codes_in_ws:
                self.ws[self.codigoLugar_cells[n+1]] = current_code
                self.ws[self.nombreLugar_cells[n+1]] = current_name.upper()
                codes_in_ws.append(current_code)

            # horas en dias - Se le suma 1 al code index porque la primera fila es para horas base
            code_index = codes_in_ws.index(current_code)
            self.ws[self.horas_norm_cells(self.works['day'][n]-(1 if self.half==1 else 16), code_index+1)]\
                                    = (8 if self.nombre_dia(self.works['day'][n]) not in ['Sábado', 'Domingo'] else '')
            self.ws[self.horas_extra_cells(self.works['day'][n]-(1 if self.half==1 else 16), code_index+1)]\
                                    = horas_trabajo(self.works['init'][n], self.works['end'][n])
    
    def write_days_outside(self, days_and_places_outside:dict):
        self.days_and_places_outside = days_and_places_outside
        print('In process...', days_and_places_outside)
        pass

    def write_non_worked_days(self, non_worked:dict):
        self.non_worked = non_worked
        print('In process...', non_worked)
        pass

    def complete_calendar_hours(self):
        for day, day_cell in enumerate([self.horas_norm_cells(x, 0) for x in range(len(self.dias_cols))]):
            if self.nombre_dia(day+1) not in ['Sábado', 'Domingo']:
                if day+1 not in self.works['day']:
                    if day+1 not in self.non_worked.keys():
                        if day+1 not in self.days_and_places_outside.keys():
                            self.ws[day_cell] = 8


if __name__ == "__main__":
    dist_wb = Distribution(3, 1, './Excel Books/payroll_layout')
