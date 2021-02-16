PLANTILLA_TX = {
    'hojas': {
        'fp_tanque': ('Cap. y FP del tanque', 6),
        'fp_c1': ('Cap. y FP Bushing C1', 5),
        'fp_c2': ('Cap. y FP Bushing C2', 7),
        'r_ais': ('Resistencia de Aislamiento', 13),
        'ttr': ('Relación de Vueltas (TTR)', 7),
        'corr_exit': ('Corriente de Excitación', 7),
        'r_dev': ('Resistencia DC del Devanado', 9),
        'alarmas': ('Alarmas y Disparos', 6),
    },
}

PLANTILLA_INT = {}

PLANTILLA_TTX = {}

PLANTILLA_RX = {}

PLANTILLA_CT = {}

PLANTILLA_PT = {}

PLANTILLA_IR = {}

PLANTILLA_OIL = {}

PLANTILLA_PARARRAYOS = {}

tipo = {
    'Transformador': PLANTILLA_TX,
    'Interruptor': PLANTILLA_INT,
    'Transformador de Tierra': PLANTILLA_TTX,
    'Reactor': PLANTILLA_RX,
    'Transformador de Corriente': PLANTILLA_CT,
    'Transformador de Voltaje': PLANTILLA_PT,
    'Historial Termográfico': PLANTILLA_IR,
    'Análisis de Aceite': PLANTILLA_OIL,
    'Pararrayos': PLANTILLA_PARARRAYOS
}