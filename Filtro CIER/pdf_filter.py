import pandas as pd
from pathlib import Path
from shutil import copy
from typing import Dict

main_path = Path('C:\\Users\\Samuel\\Desktop\\CIER FASE VI EVENTOS AÑOS 2017 2018 y 2019')
file_name_template = main_path/'SEGUIMIENTO_EVENTOS year.xlsx'
results_path = main_path/'final results'
not_found = results_path/'no ETESA'
year_results_path = lambda year: results_path/str(year)

files: Dict[int, pd.DataFrame] = {}
for year in range (2017, 2020):
    current_name = file_name_template.__str__().replace('year', str(year))
    f = pd.read_excel(current_name, f'EVENTOS_{year}', header=1)
    files[year] = f
    files[year]['has_pdf'] = False


for year in range(2017, 2020):
    year_path = main_path/str(year)
    for file in year_path.rglob('IE*.pdf'):
        num = None
        try:
            num = int(file.name[2:5])
            # print(num)
        except Exception as e:
            try:
                num = int(file.name[2:4])
            except Exception as e:
                print(f'ERROR IN FILE {file.name}.', e)
        
        if num in files[year]['EVENTO'].values:
            copy(file, year_results_path(year)/file.name)
            files[year].loc[files[year]['EVENTO']==num, 'has_pdf'] = True
            print(f'File {num} is in {year} Excel')
        else:
            copy(file, not_found/file.name)
            print(f'File {num} is not in {year} Excel')

for year, file in files.items():
    file.to_excel(results_path/(str(year)+'.xlsx'), sheet_name='RESULTS')
