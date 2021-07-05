from pdf_filter import pdf_filter
from get_events_dict import get_events_dict
from make_txt import make_events_txt
from indicators_calc import IndicatorCalc
from add_equipments_to_durations import add_equipments_to_time_pdf

from pathlib import Path
from typing import Dict

CIER_FILES_PATH = 'C:\\Users\\Samuel\\Desktop\\CIER FASE VI EVENTOS AÑOS 2017 2018 y 2019\\filtered results'
main_path = Path(CIER_FILES_PATH)

events_dict:Dict[str, Dict[str, str]] = get_events_dict(main_path)

init_str = 'EQUIPOS AFECTADOS'
final_str = 'AGENTES INVOLUCRADOS'
limit_tuple = init_str, final_str
affected_equipment = pdf_filter(events_dict, limit_tuple = limit_tuple)

# Add affected equipment to data
# duration_path = main_path / 'Resultados de Duracion.xlsx'
# add_equipments_to_time_pdf(duration_path, equipments_dict=affected_equipment)

# make_events_txt('filtro_por_equipos', affected_equipment)

# Get indicator calc
calc = IndicatorCalc()

# print('TMI DATA: ')
libranzas_path = main_path / 'libranzas'
tmi_data = calc.get_tmi_data_per_year(libranzas_path)
# calc.print_indicator_dict(tmi_data)

# print('TMT DATA: ')
events_path = main_path / 'Resultados de Duracion.xlsx'
tmt_data = calc.get_tmt_data_per_year(events_path)
# calc.print_indicator_dict(tmt_data)

for yr, data in tmi_data.items():
    for fam in data[1].keys():
        print(f'Para {fam} del año {yr}:')
        print(tmi_data[yr][1][fam])
        print(tmt_data[yr][1][fam], end='\n\n')


