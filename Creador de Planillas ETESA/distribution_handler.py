# Tienes que anadir aqui los cambios a hacer en distribucion sheet
def dist_data():
    nombre_cell = 'F:7'
    cedula_cells = [f'{chr(i)}:6' for i in range(ord('S'), ord('Z')+1)]\
                    + [f'A{chr(i)}:6' for i in range(ord('A'), ord('C')+1)]
    numEmpleado_cell = 'W:7'
    gerencia_cell = 'F:8'
    depto_cell = 'W:8'
    cargo_cell = 'F:9'
    periodo_cells = ['Y:9','AB:9']

    lugarInit_cols = [col for col in range(17, 21+1)]
    dias_cols = [f'{chr(i)}' for i in range(ord('Q'), ord('Z')+1)]\
                + [f'A{chr(i)}' for i in range(ord('A'), ord('H')+1)]
    codigoLugar_col = ''

    tareaInit_rows = [col for col in range(25, 33+1)]
    tarea_col = ''
    inicioFin_cols = ['','']

    enfermedad_row = '37'
    fiestaDuelo_row = '38'
    accidente_row = '39'
    adiestram_row = '40'
    vacaciones_row = '41'
    compensatiorio_row = '42'
    sindical_row = '43'
    otros_row = '44'