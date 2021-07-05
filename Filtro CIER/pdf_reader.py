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
target_information = 'Duración del Evento'
next_information = 'Tipo de Evento'

# get event data needed variables
data_format = '%d-%b-%Y  %H:%M:%S'
duration_format = '%H:%M:%S'


@dataclass
class EventDate:
    start: datetime = datetime.now()
    end: datetime = datetime.now()

    @property
    def duration(self) -> timedelta:
        return self.end - self.start
    
    def __repr__(self) -> str:
        return f'start: {self.start}, end: {self.end}, Minutes duration: {int(self.duration.seconds/60)}'

    def set_start_date(self, time:str, format:str) -> None:
        self.start = datetime.strptime(time, format)

    def set_end_date(self, time:str,  format:str) -> None:
        self.end = datetime.strptime(time, format)

    def get_start_date_formatted(self, format:str):
        return self.start.strftime(format)

    def get_end_date_formatted(self, format:str):
        return self.start.strftime(format)

    def get_duration_time_hours(self):
        return self.duration.total_seconds()/3600
    
    def get_duration_time_minutes(self):
        return self.duration.total_seconds()/60
    
    def get_duration_time_seconds(self):
        return self.duration.total_seconds()
    
    def get_duration_str(self, format) -> str:
        hours = int(self.duration.total_seconds()/3600)
        mins = int(self.duration.total_seconds()/60) - hours*60
        secs = int(self.duration.total_seconds()) - hours*3600 - mins*60
        try:
            time = datetime.now().replace(hour=hours, minute=mins, second=secs)
            return time.strftime(format)
        except Exception:
            time = datetime.now().replace(minute=mins, second=secs)
            return str(hours)+time.strftime(format)[2:]


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

        # Para fechas con el mes sin punto
        if '.' not in result:
            result = format_time_result(result)

        if find_after_next:
            after = text[final_index+len(next_information):final_index+len(next_information)+len(next_format)]
            if after.startswith('\n'):
                after = text[final_index+len(next_information)+1:final_index+len(next_information)+len(next_format)+1]
            return (result, after)
        else:
            return result

def format_time_result(result:str):
    print('Fixing', result, '...')
    idx = result.find('-', 6)
    idx2 = result.find('-', 27)
    return result[:idx] + '.' + result[idx:idx2] + '.' + result[idx2:]

def get_event_date_data(info:str, data_format) -> EventDate:
    date_len = len(info)//2
    start_date = info[:date_len]
    end_date = info[date_len:2*date_len]

    result = EventDate()
    try:
        result.set_start_date(start_date, data_format)
        result.set_end_date(end_date, data_format)
    except Exception as e:
        print(f'Error in formatting {info}. Trying with new format...', e)
        result.set_start_date(start_date, data_format[:-2])
        result.set_end_date(end_date, data_format[:-2])

    return result

results_dict = {}

index_count = 0
for year in range(2017, 2020):
    for file in year_files_path(year).glob("*.pdf"):
        info, duration = find_information(file, target_information, next_information, find_after_next=True, next_format=duration_format)

        try:
            result = get_event_date_data(info, data_format=data_format)
            start_event = str(result.start)
            end_event = str(result.end)
            duration_str = result.get_duration_str(duration_format)
            minutes = result.get_duration_time_minutes()

        except Exception as e:
            print(f'Error in {file.name}: {e}')
            start_event = info[:len(info)//2]
            end_event = info[len(info)//2:]
            duration_str = 'Error in time'
            minutes = 'Error in time'

        dct = {
            'event': (file.name[2:5] if file.name[2:5].isnumeric() else file.name[2:4]),
            'filename': file.name,
            'year': str(year),
            'start_event': start_event,
            'end_event': end_event,
            'file_duration': duration,
            'calculated_duration': duration_str,
            'minutes_duration': minutes,
            'calculated_equals_file': duration == duration_str
        }

        results_dict[index_count] = dct
        index_count += 1

df = pd.DataFrame(results_dict.values(), index=results_dict.keys())
print(df)

# df.to_excel(results_path/'duration_results.xlsx', 'DURATIONS')


