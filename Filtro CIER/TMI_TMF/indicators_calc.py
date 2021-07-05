from pathlib import Path
from typing import Dict
import pandas as pd
from collections import namedtuple, defaultdict

class IndicatorCalc:
    get_year_from_name = lambda string: [year for year in range(2017, 2020) if str(year) in string][0]

    def get_tmt_data_per_year(self, duration_file_path:Path,
            minute_duration_col = 'minutes_duration') -> dict:
        
        result_dict = {}
        duration_col = minute_duration_col  # Recordar cambiar a horas

        events_df:pd.DataFrame = pd.read_excel(duration_file_path, sheet_name='DURATIONS')

        tmt_info = {
            ('lineas 115', '115'),
            ('lineas 230', '230'),
            ('capacitores 115', '11C'),
            ('capacitores 230', '23C'),
            ('transformadores', ('T1', 'T2', 'T3', 'T4', 'T5', 'T6')),
            ('reactores', ('R1', 'R2', 'R3', 'R4', 'R5', 'R6')),
        }

        for year in events_df['year'].drop_duplicates().sort_values(ascending=True):
            # TMT Calc
            tmt_tuple = namedtuple('TMT', ['hmni', 'nmcf', 'result'])
            tmt_dct = defaultdict(tmt_tuple)
            is_year = events_df['year']==int(year)

            for key, pattr in tmt_info:

                if type(pattr) == tuple:
                    filtr = events_df['equipment'].str.contains(pattr[0])
                    for string in pattr:
                        filtr |= events_df['equipment'].str.contains(string)

                else:
                    filtr = events_df['equipment'].str.contains(pattr)

                df:pd.DataFrame = events_df.loc[is_year & filtr]
                hmni:pd.Timedelta = df[duration_col].sum()
                hmni:float = hmni/60
                nmfc = df.__len__()
                res = hmni/nmfc if nmfc > 0 else 0
                tmt_dct[key] = tmt_tuple(hmni, nmfc, res)

            print(df)
            result_dict[year] = df, tmt_dct
        
        return result_dict



    def get_tmi_data_per_year(self, libranzas_folder:Path, 
            hour_cols = ('Fecha Inicio Real', 'Fecha Final Real', 'Duración Real')) -> dict:

        get_year_from_name = lambda string: [year for year in range(2017, 2020) if str(year) in string][0]
        time_fmt = '%d/%m/%Y %H:%M'
        result_dict = {}

        init_col, final_col, duration_col = hour_cols

        for file in libranzas_folder.glob('*.xlsx'):
            libranzas_df:pd.DataFrame = pd.read_excel(file, sheet_name='Reporte', header=1)
            libranzas_df.loc[:, init_col] = pd.to_datetime(libranzas_df[init_col], format=time_fmt)
            libranzas_df.loc[:, final_col] = pd.to_datetime(libranzas_df[final_col], format=time_fmt)
            libranzas_df.loc[:, duration_col] = libranzas_df[final_col] - libranzas_df[init_col]

            # TMI Calc
            tmi_tuple = namedtuple('TMI', ['hmi', 'nmcf', 'result'])
            tmi_dct = defaultdict(tmi_tuple)
            
            # Filters
            equip = libranzas_df['Equipos']
            emerg = libranzas_df['Tipo']=='Emergencia'
            
            tmi_info = {
                ('lineas 115', ': 115'),
                ('lineas 230', ': 230'),
                ('capacitores 115', ': 11C'),
                ('capacitores 230', ': 23C'),
                ('transformadores', ': T'),
                ('reactores', ': R'),
            }

            for key, pattr in tmi_info:
                filtr = equip.str.contains(pattr)
                df:pd.DataFrame = libranzas_df.loc[emerg & filtr]
                hmi:pd.Timedelta = df[duration_col].sum()
                hmi:float = hmi.total_seconds()/3600
                nmfc = df.__len__()
                res = hmi/nmfc if nmfc > 0 else 0
                tmi_dct[key] = tmi_tuple(hmi, nmfc, res)

            name = get_year_from_name(file.name)
            result_dict[name] = libranzas_df, tmi_dct
        
        return result_dict

    def print_indicator_dict(self, indicator_data: dict) -> None:
        for year, data in indicator_data.items():
            print(f'Para el año {year}:')
            for fam, tup in data[1].items():
                print(f'\t{fam}:')
                print(f'\t{tup}')
                print(f'\t\tANS: {tup[2]}')
                print(f'\t\t\tNUMERADOR: {tup[0]}')
                print(f'\t\t\tDENOMINADOR: {tup[1]}')

if __name__ == "__main__":
    filepath = Path('C:\\Users\\Samuel\\Desktop\\CIER FASE VI EVENTOS AÑOS 2017 2018 y 2019\\filtered results\\libranzas')
    
    calc = IndicatorCalc()
    tmi_data_per_year = calc.get_tmi_data_per_year(filepath)
    calc.print_indicator_dict(tmi_data_per_year)

            