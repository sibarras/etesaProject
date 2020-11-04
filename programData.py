
tests = [
    'Tiempos de Operación',             #0
    'Resistencia de Contacto',          #1
    'Resistencia de Aislamiento',       #2
    'Resistencia de Devanados',         #3
    'Relación de Vueltas',              #4
    'Factor de Potencia',               #5
    'Análisis de Gas SF6',              #6
    'Análisis de Calidad de Energía',   #7
    'Corriente de Excitación',          #8
    'Saturación',                       #9
    'Alarmas',                          #10
    'Disparos',                         #11
    'Bloqueos',                         #12
    'Tratamiento de gas SF6',           #13
    'Collar Caliente',                  #14
    'Inspección Termográfica',          #15
    'Surge Arrest',                     #16
    'Pruebas Eléctricas',               #17
]


equipmentGeneralTest = {
    'PT': [tests[i] for i in [17]],
    'CT': [tests[i] for i in [17]],
    'INT': [tests[i] for i in [17, 13, 10, 12]],
    'TX': [tests[i] for i in [17, 10, 11]],
    'RX': [tests[i] for i in [17, 10, 11]],
    'TTX': [tests[i] for i in [17, 10, 11]],
    'Pararrayos': [tests[i] for i in [17]],
    'Termo': [tests[i] for i in [15]]
}

nombres_generales = {
    'PT': 'Transformador de Voltaje',
    'CT': 'Transformador de Corriente',
    'INT': 'Interruptor',
    'TX': 'Transformador',
    'RX': 'Reactor',
    'TTX': 'Transformador de Tierra',
    'Pararrayos': 'Grupo de Pararrayos',
    'Termo': 'Patio de 230 y 115'
}

equipmentTests = {
    'PT': [tests[i] for i in [5, 2]],
    'CT': [tests[i] for i in [2, 3, 4, 5, 8, 9]],
    'INT': [tests[i] for i in [0, 1, 6, 10, 12]],
    'TX': [tests[i] for i in [5, 8, 4, 3, 10, 11]],
    'RX': [tests[i] for i in [5, 3, 10, 11]],
    'TTX': [tests[i] for i in [8, 5, 3, 10, 11]],
    'Pararrayos': [tests[i] for i in [16, 2]],
    'Termo': [tests[15]]
}

se = 'Subestación '
nombre_SE = {
    'SPANAMA2': se+'Panamá II',
    'SPANAMA': se+'Panamá',
    'SCHORRE': se+'Chorrera',
    'SCACERE': se+'Cáceres',
    'SLLSANC': se+'Llano Sánchez',
    'SSTA RITA': se+'Santa Rita',
    'SVELADER': se+'Veladero',
    'SMDN': se+'Mata de Nance',
    'SPROGRE': se+'Progreso',
    'SGUASQU': se+'Guasquitas',
    'SCALDER': se+'Caldera',
    'SCHAZUL': se+'Charco Azul',
    'SCHANGU': se+'Changuinola',
    'SCHILIB': se+'Chilibre',
    'CVALES': se+'Los Valles',
    'CESTREL': se+'La Etrella',
    'CPACORA': se+'Pacora',
    'CBLM1': se+'Bahía Las Minas',
    'CPAN AM': se+'PANAM',
    'CESTI': se+'Estí',
    'CFORT': se+'Fortuna',
    'CBLM': se+'Bahía Las Minas',
    'CBAYAN': se+'Bayano',
    'SBARTOLO': se+'San Bartolo',
    'SHIGO': se+'El Higo'
}
del se

spanishDict = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miercoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sabado',
    'Sunday': 'Domingo',
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}