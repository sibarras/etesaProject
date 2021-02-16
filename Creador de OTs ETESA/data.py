SE = ''
places_id = {
    SE+'Charco Azul':'SE-CHAZUL',
    SE+'Caldera':'SE-CALDRA',
    SE+'Santa Rita':'SE-STARTA',
    SE+'Changuinola':'SE-CHGLA',
    SE+'Guasquitas':'SE-GUAQTA',
    SE+'Progreso':'SE-PROG',
    SE+'Mata de Nance':'SE-MAN',
    SE+'Veladero':'SE-VLDRO',
    SE+'Bahía Las Minas':'SE-BLM',
    SE+'Llano Sánchez':'SE-LL-SZ',
    SE+'Bayano':'SE-BYNO',
    SE+'Chorrera':'SE-CHO',
    SE+'Cáceres':'SE-CAC',
    SE+'Panamá':'SE-PAN',
    SE+'Panamá II':'SE-PAN2',
    SE+'San Bartolo': 'SE-SBA',
    SE+'Los Valles': 'SE-LVALLES',
    SE+'La Estrella': 'SE-LESTRLA',
    SE+'La Esperanza': 'SE-LAESPE',
    SE+'El Higo': 'SE-HIG',
    SE+'Fortuna': 'SE-FORTNA',
    SE+'Cañazas': 'SE-CNZAS',
    SE+'Boquerón III': 'SE-BOQUERON',
    SE+'Bella Vista': 'SE-MAN'
}

se = ''
substation_account_realname = {
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
    'CLVALES': se+'Los Valles',
    'CESTREL': se+'La Etrella',
    'CPACORA': se+'Pacora',
    'CBLM1': se+'Bahía Las Minas 1',
    'CPAN AM': se+'PANAM',
    'CESTI': se+'Estí',
    'CFORT': se+'Fortuna',
    'CBLM': se+'Bahía Las Minas',
    'CBAYAN': se+'Bayano',
    'SBARTOLO': se+'San Bartolo',
    'SHIGO': se+'El Higo',
}
del se

tools_dict = {
    'Multimetro Digital': 49008,            #0
    'Termografia': 7199,                    #1
    'Rigidez Dielectrica': 7213,            #2
    'Medidor Punto de Rocio': 7210,         #3
    'Probador de CT': 7235,                 #4
    'Probador de Factor de Potencia': 7195, #5
    'Resistencia de Devanado': 7210,        #6
    'Resistencia de Aislamiento': 7191,     #7
    'Calibrador TTR': 7196,                 #8
    'Resistencia de Contacto': 7202,        #9
    'Analizador de Interruptores': 7205,    #10
    'Medidor de Humedad': 7209,             #11
    'Resistencia a Tierra': 7220,           #12
    'Hi-Pot': 7232,                         #13
    'Analizador H2': 7236,                  #14
    'Analizador de Potencia': 7244,         #15
    'Bomba de Vacio': 6396,                 #16
    'Compresor de Aire': 6397,              #17
    'Herramientas de Mano': 866             #18
}

tools_id = list(tools_dict.values())

work_tools = {
    'PT': [tools_id[i] for i in [0, 5]],
    'CT': [tools_id[i] for i in [4, 5, 0]],
    'INTERRUPTOR': [tools_id[i] for i in [10, 9, 11, 0]],
    'TX': [tools_id[i] for i in [5, 6, 8, 7, 0]],
    'RX': [tools_id[i] for i in [5, 6, 7, 0]],
    'TTX': [tools_id[i] for i in [5, 6, 7, 0]],
    'PARARRAYOS': [tools_id[i] for i in [5, 7]],
    'TERMOGRAFIA': [tools_id[i] for i in [1]],
    'INSPECCION': [tools_id[i] for i in []],
    'COMISIONADO': [tools_id[i] for i in []],
    'VIAJE': [tools_id[i] for i in []],
    'RIGIDEZ DIELECTRICA': [tools_id[i] for i in [2]],
    'CALIDAD ENERGIA': [tools_id[i] for i in [15]],
    'ANALISIS SF6': [tools_id[i] for i in [11]],
    'OTROS': [tools_id[i] for i in []],
}

class WorkDetails:
    name:str
    priority:str
    duration:str
    tools:str


work_details = {
    'SUBESTACIÓN':{
        'Prioridad':'1',
        'Duracion': '4:00',
        'Herramientas': 'TERMOGRAFIA'
    },
    'RED DE PUESTA A TIERRA':{
        'Prioridad':'5',
        'Duracion': '5:00',
        'Herramientas': ''
    },
    'TRANSFORMADOR DE POTENCIA':{
        'Prioridad':'9',
        'Duracion': '10:00',
        'Herramientas': 'TX'
    },
    'TRANSFORMADOR DE CORRIENTE':{
        'Prioridad':'5',
        'Duracion': '7:00',
        'Herramientas': 'CT'
    },
    'INTERRUPTOR':{
        'Prioridad':'5',
        'Duracion': '7:00',
        'Herramientas': 'INTERRUPTOR'
    },
    'LÍNEA':{
        'Prioridad':'1',
        'Duracion': '4:00',
        'Herramientas': 'CALIDAD ENERGIA'
    },
    'TRANSFORMADOR DE ATERRIZAJE':{
        'Prioridad':'5',
        'Duracion': '7:00',
        'Herramientas': 'TTX'
    },
    'BARRA':{
        'Prioridad':'1',
        'Duracion': '4:00',
        'Herramientas': 'CALIDAD ENERGIA'
    },
    'REACTOR ':{
        'Prioridad':'5',
        'Duracion': '7:00',
        'Herramientas': 'RX'

    },
    'OTRO':{
        'Prioridad':'1',
        'Duracion': '4:00',
        'Herramientas': ''
    }
}

special_works_keys = {
    'TRANSFORMADOR DE POTENCIA': {
        'name':'TOMA DE MUESTRA DE ACEITE',
        'tool_key': 'RIGIDEZ DIELECTRICA'
    },
    'INTERRUPTOR': {
        'name':'ANÁLISIS DE GAS SF6',
        'tool_key': 'ANALISIS SF6',
    },
}

workers = {
    'ZONA 1': ['mperez', 'psolis', 'sibarra'],
    'ZONA 3': ['mmartinez', 'faguirre'],
    'ESPECIAL': ['jbmartinez', 'sibarra']
}

special_works_for_workers = [
    'TRANSFORMADOR DE POTENCIA', 'TRANSFORMADOR DE ATERRIZAJE',
    'REACTOR', 'CT'
]
