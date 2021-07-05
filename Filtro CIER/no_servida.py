from typing import Union
import PyPDF2
from PyPDF2.pdf import PageObject
import pandas as pd
import numpy as np

from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass
import locale

from os import mkdir
from shutil import copy

# to read spanish dates
locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

# to find path
main_path = Path('C:\\Users\\Samuel\\Desktop\\CIER FASE VI EVENTOS AÑOS 2017 2018 y 2019')
results_path = main_path/'final results'
year_files_path = lambda year: results_path/str(year)

# Find information needed variables
target_information = 'ENERGÍA NO SERVIDA'
next_information = 'PROTECCIONES'

# get event data needed variables
data_format = '%d-%b-%Y  %H:%M:%S'
duration_format = '%H:%M:%S'



def find_information(pdf_path:Path, target_information:str, next_information:str,
                    find_after_next: bool= False, next_format:str='') -> Union[str, tuple[str, str]]:

    with open(pdf_path, 'rb') as f:

        # Leo el archivo
        file = PyPDF2.PdfFileReader(f)

        # Compruebo si tiene mas de una pagina y selecciono la primera pagina
        if file.getNumPages() > 0:
            page:PageObject = file.getPage(0)
        else:
            raise FileNotFoundError

        # Extraigo el texto del pdf
        text = page.extractText()
        

        # Encuentro el punto donde se encuentra el titulo de mi informacion deseada
        index = text.find(target_information)
        final_index = text.find(next_information)


        # Recorto solo lo que necesito
        result = text[index+len(target_information):final_index]

        if len(result) == 4:
            result = text[index+len(target_information):]

        return result

results_dict = {}
index_count = 0

for year in range(2017, 2020):


    print(year_files_path(year))


    for file in year_files_path(year).glob("*.pdf"):
        info = find_information(file, target_information, next_information, next_format=duration_format)

        dct = {
            'EVENTO': (file.name[2:5] if file.name[2:5].isnumeric() else file.name[2:4]),
            'Nombre': file.name,
            'Año': str(year),
            'No Servida': info,
            'Verificar': len(info) == 4
        }

        results_dict[index_count] = dct
        index_count += 1

df = pd.DataFrame(results_dict.values(), index=results_dict.keys())
print(df)

df.to_excel(results_path/'resultados_no_servida.xlsx', 'NO SERVIDA')

