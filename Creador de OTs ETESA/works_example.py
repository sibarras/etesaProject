from works_struc import PMAWork
work_example = {
    'Titulo': 'Inspección Termográfica en Subestación Panamá II',
    'Libranza': '',
    'OT': '',
    'Ubicacion': 'Panamá II',
    'Tipo': 'MPD',
    'Clasificacion': 'PMA',
    'Cuenta': '1.51121200.0601.430403.430403.0.0000.0.0000',
    'Prioridad': '1',
    'Inicio': '02/15/2021 10:30 AM',
    'Duracion': '4:00',
    'Supervisor': 'JBMARTINEZ',
    'Mano de Obra': [
        'sibarra',
        'mperez'
    ],
    'Herramientas': 'TERMOGRAFIA'
}

work_object = PMAWork()
work_object.titulo = work_example['Titulo']
work_object.libranza = work_example['Libranza']
work_object.ot = work_example['OT']
work_object.ubiacion = work_example['Ubicacion']
work_object.tipo = work_example['Tipo']
work_object.clasificacion = work_example['Clasificacion']
work_object.cuenta = work_example['Cuenta']
work_object.prioridad = work_example['Prioridad']
work_object.inicio = work_example['Inicio']
work_object.duracion = work_example['Duracion']
work_object.supervisor = work_example['Supervisor']
work_object.mano_de_obra = work_example['Mano de Obra']
work_object.herramientas = work_example['Herramientas']

works = [work_object]
