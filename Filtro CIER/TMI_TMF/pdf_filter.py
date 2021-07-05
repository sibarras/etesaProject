from typing import Dict, Tuple
from PyPDF2 import utils

from PyPDF2.pdf import PageObject
from get_events_dict import get_events_dict
from make_txt import make_events_txt
from pathlib import Path
import PyPDF2


def pdf_filter(events_dict: dict, limit_tuple: Tuple[str, str]) -> dict:
    res_dict = events_dict.copy()
    for year, events in events_dict.items():
        for event_number, event_path in events.items():

            try:
                reader = PyPDF2.PdfFileReader(event_path)
                page:PageObject = reader.getPage(0)
                text = page.extractText()
                
                init_str, final_str = limit_tuple
                init_idx = text.index(init_str) + len(init_str)
                final_idx = text.index(final_str)

                result = text[init_idx:final_idx]
                res_dict[year][event_number] = result

            except utils.PyPdfError as e:
                print(f'ERROR IN {event_number} OF YEAR {year}:', e)
                res_dict[year][event_number] = "ERROR: "+ e.__str__()

    return res_dict


if __name__ == "__main__":
    CIER_FILES_PATH = 'C:\\Users\\Samuel\\Desktop\\CIER FASE VI EVENTOS AÑOS 2017 2018 y 2019\\final results'
    main_path = Path(CIER_FILES_PATH)

    events_dict:Dict[str, Dict[str, str]] = get_events_dict(main_path)

    init_str = 'EQUIPOS AFECTADOS'
    final_str = 'AGENTES INVOLUCRADOS'
    limit_tuple = init_str, final_str
    affected_equipment = pdf_filter(events_dict, limit_tuple = limit_tuple)

    make_events_txt('filtro_por_equipos', affected_equipment)

    # for events in affected_equipment.values():
    #     print()
    #     for equipments in events.values():
    #         print(equipments, end='\n')

            
        
