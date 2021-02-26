from typing import Reversible
import pandas as pd
from pathlib import Path
import sqlite3
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from functools import reduce
from random import choice, sample

from data import work_details, places_id, substation_account_realname,\
                special_works_keys, workers, special_works_for_workers
from works_example import work_example
from works_struc import PMAWork

class PMADataset:

    def __init__(self, db_name:Path) -> None:

        self.db_name = Path(db_name)

        self.TABLE = 'pma_data'
        self.pma_df:pd.DataFrame
        self.works_df:pd.DataFrame
        self.work_list:list = []


        self.pma_df = self.read_data()

# initial functions
    def read_data(self) -> pd.DataFrame:

        if Path(self.db_name).exists():
            # Read table
            pma_df = self.read_db(self.db_name)

        else:
            # Ask for file to use
            root = tk.Tk()
            root.withdraw()
            file_path = Path(filedialog.askopenfilename())
            excel = pd.ExcelFile(file_path)

            # Ask for sheet to use
            print(f'Sheet Names inside {file_path.name}:')
            for n, name in enumerate(excel.sheet_names):
                print(f'{n+1}. {name}')
            index = int(input('\nChoose one Sheet Name: '))
            assert 0 < index < len(excel.sheet_names)+1
            sheet_name = excel.sheet_names[index-1]

            # Read Excel
            header = 15
            usecols = range(16)
            skiprows_fn = lambda x:x>=304
            pma_df = pd.read_excel(file_path, sheet_name, header=header-1,
                                    usecols=usecols, skiprows=skiprows_fn)

            # Create db
            self.create_db(self.db_name, self.TABLE, pma_df)
        
        return pma_df

    def read_db(self, db_name) -> pd.DataFrame:
        with sqlite3.connect(db_name) as conn:
            print('Reading existing db...')
            pma_df = pd.read_sql_query(f"SELECT * FROM {self.TABLE}", conn, index_col='index')
            print('Reading Done!')
            return pma_df

    def create_db(self, db_name, table_name, content:pd.DataFrame) -> None:
        # Create db
        with sqlite3.connect(db_name) as conn:
            print('Creating new db file...')
            content.to_sql(table_name, conn, index=True)
            print('db creation done!\n')

    def add_works_to_df(self, work_details=work_details) -> pd.DataFrame:
        print('Adding work complements to works dataframe...')
        types = self.pma_df['TIPO DE EQUIPO']
        details_df = pd.DataFrame()

        for detail in work_details[types[0]].keys():

            detail_list = [work_details[type][detail] for type in types]
            details_df[detail.upper()] = detail_list
        
        self.pma_df = self.pma_df.join(details_df)
        print('PMA dataframe completed!\n')

# df validation functions
    def validate_place_keys(self) -> bool:
        assert len(list(self.pma_df.iloc)) > 0
        case_1 = len(list(filter(lambda x: self.__normalize(x) not in places_id, self.pma_df['SUBESTACION']))) == 0
        return case_1
    
    def validate_tools_keys(self) -> bool:
        list1 =self.pma_df['TIPO DE EQUIPO'].drop_duplicates().to_list()
        list2 = list(work_details.keys())
        return set(list1).issubset(list2)
    
    def __needed_databases_exists(self):
        db_path = self.db_name.parent
        return self.db_name.exists() and (db_path/'accounts.db').exists()
    
    def __normalize(self, sub):
        return sub.title()\
                .replace('Iii', 'III')\
                .replace('Ii', 'II')\
                .replace('De', 'de')\
                .replace('Sanchez', 'Sánchez')\
                .strip()
    
    def __to_work_title(self, work_title:str):
        return work_title.title()\
                    .replace('Sf6 ', 'SF6 ').replace('A ', 'a ').replace('De ', 'de ')\
                    .replace('En ', 'en ').replace('Y ', 'y ').replace('Tt', 'TT')\
                    .replace('Iii', 'III').replace('Ii', 'II').replace('None', '')\
                    .replace('  ', ' ').replace('a La Subestación a Subestación ', '')\
                    .replace('Puesta a Tierra a Red de Puesta', 'Red de Puesta')\
                    .replace('SF6 Interruptores Bancos', 'SF6 Asociado a los Bancos')\
                    .replace('SF6 Interruptores Reactores', 'SF6 Asociado a los Reactores')\
                    .replace('Potencia Todos en', 'Potencia en')\
    
    def __accounts_data_exists(self, works_data, accounts_data):
        return set(works_data).issubset([substation_account_realname[acc].upper() for acc in accounts_data])

# df creator
    def set_works_df(self) -> pd.DataFrame:
        print('Creating works dataframe... This is the main dataset.')
        assert self.__needed_databases_exists()
        works_df = pd.DataFrame()
        pma_lenth = len(self.pma_df)
        singlevalue_list = lambda x, l: [x for _ in range(l)]
        needed_columns = [kys.upper() for kys in work_example.keys()]
        
        # Adicional a lo existente, se necesita crear un titulo, cuenta, fecha, supervisor, mano de obra

        # Title
        columns = ['DESCRIPCION DEL TRABAJO', 'TIPO DE EQUIPO', 'DESCRIPCION DE EQUIPO', 'SUBESTACION']
        assert set(columns).issubset(list(self.pma_df.keys()))
        works_df['TITULO'] = [
            self.__to_work_title(f"{i[columns[0]]} a {i[columns[1]]}"+
                                f" {i[columns[2]]} en Subestación {i[columns[3]]}")
            for i in self.pma_df.iloc
        ]

        # Libranza y OT
        works_df['LIBRANZA'] = singlevalue_list('', pma_lenth)
        works_df['OT'] = self.pma_df['Numero de OT']

        # Ubicacion
        works_df['UBICACION'] = self.pma_df['SUBESTACION']

        # Tipo y Clasificacion
        works_df['TIPO'] = singlevalue_list('MPD', pma_lenth)
        works_df['CLASIFICACION'] = singlevalue_list('PMA', pma_lenth)

        # Accounts
        work_ubication_key = 'SUBESTACION'
        account_ubication_key = 'UBICAC'
        account_code_key = 'UBC'
        accounts_db_name = self.db_name.parent/'accounts.db'
        create_complete_account = lambda acc: f'1.51121200.{(4-len(acc))*"0"}{acc}.430403.430403.0.0000.0.0000'
    
        with sqlite3.connect(accounts_db_name) as conn:
            accounts_df = pd.read_sql_query('SELECT * FROM accounts', conn, index_col='index')
        
        workplaces_with_accounts = self.pma_df[work_ubication_key]\
            .replace(['LA ESPERANZA', 'BELLA VISTA', 'CAÑAZAS', 'BOQUERÓN III'], 'MATA DE NANCE')
        
        assert self.__accounts_data_exists(workplaces_with_accounts, accounts_df[account_ubication_key])

        accounts_df[account_ubication_key] = [
            substation_account_realname[acc].upper() for acc in accounts_df[account_ubication_key]
        ]
        works_df['CUENTA'] = [create_complete_account(accounts_df.loc[accounts_df[account_ubication_key]==sub]\
                             [account_code_key].values[0]) for sub in workplaces_with_accounts]
        
        # Priority and Duration
        works_df['PRIORIDAD'] = self.pma_df['PRIORIDAD']
        works_df['DURACION'] = self.pma_df['DURACION']

        short_works_duration = '1:00'
        short_works_priority = 1

        for equip, work in special_works_keys.items():
            # using only first in list for locator. Iterate the list in the future.
            locator = self.pma_df['DESCRIPCION DEL TRABAJO']\
                    .str.startswith(work['name'])
            length = len(works_df.loc[locator, 'DURACION'])
            works_df.loc[locator, 'DURACION'] = [short_works_duration for _ in range(length)]
            works_df.loc[locator, 'PRIORIDAD'] = [short_works_priority for _ in range(length)]

        # Date
        parse_format = "%Y-%m-%d %H:%M:%S"
        maximo_format = "%m/%d/%Y %I:%M %p"

        dates_df = pd.DataFrame()
        pma_copy = self.pma_df.copy()
        pma_copy['DURACION'] = works_df['DURACION']
        date_needed_cols = ['ZONA', 'FECHA DE INICIO', 'DURACION', 'TIPO DE EQUIPO']
        dates_df[date_needed_cols] = pma_copy[date_needed_cols]
        dates_df['REPEATED'] = singlevalue_list(False, pma_lenth)

        set_first_time = lambda date, first_hour : datetime.strptime(date, parse_format)\
                                        .replace(hour=first_hour).strftime(parse_format)
        
        dates_df['FECHA DE INICIO'] = dates_df['FECHA DE INICIO'].apply(set_first_time, args=(8,))

        format_hour_str = lambda date, hour_delta, count: datetime.strptime(date, parse_format)\
                                        .replace(hour=datetime.strptime(date, parse_format).hour + 
                                            datetime.strptime(hour_delta, "%H:%M").hour*count
                                        ).strftime(maximo_format)

        self.count = 0
        def set_hours(item1, item2, lmdaf=format_hour_str):
            hour = '0:00'
            if item2['REPEATED'] == True:
                if item1['TIPO DE EQUIPO']!='TRANSFORMADOR DE POTENCIA' \
                and item2['TIPO DE EQUIPO']!='TRANSFORMADOR DE POTENCIA':
                    self.count += 1
                    hour = item1['DURACION']

                dates_df.loc[item2.name,'REPEATED'] = False
            else:
                self.count = 0

            dates_df.loc[item2.name,'FECHA DE INICIO'] = lmdaf(item2['FECHA DE INICIO'], hour, self.count)
            return item2

        for zona in dates_df['ZONA'].drop_duplicates().values:
            zone_locator = dates_df['ZONA'] == zona
            is_duplicated_info = dates_df.loc[zone_locator]['FECHA DE INICIO'].duplicated()
            dates_df['REPEATED'].update(is_duplicated_info)

            reduce(set_hours, dates_df.loc[zone_locator].iloc, dates_df.loc[zone_locator].iloc[0])

        works_df['INICIO'] = dates_df['FECHA DE INICIO']

        # Supervisor
        works_df['SUPERVISOR'] = singlevalue_list('JBMARTINEZ', pma_lenth)

        # Workers
        special_elem_list = special_works_for_workers

        def set_workers(work_row):
            if work_row['TIPO DE EQUIPO'] in special_elem_list or work_row['ZONA']==2:
                return special_choice(work_row, workers)
        
            work_row['MANO DE OBRA'] = sample(workers[f'ZONA {work_row["ZONA"]}'], 2)
            return work_row

        def special_choice(work_row, workers_dict):
            selection = [choice(workers_dict['ESPECIAL'])]
            while True:
                selection.append(choice(workers_dict[choice(['ZONA 1', 'ZONA 3'])]))
                if selection[0] != selection[1]:
                    break
                selection.pop()
            work_row['MANO DE OBRA'] = selection
            return work_row

        workers_df = self.pma_df[['TIPO DE EQUIPO', 'ZONA']].copy()
        workers_df['MANO DE OBRA'] = singlevalue_list('', pma_lenth)
        workers_df = workers_df.apply(set_workers, axis=1)

        works_df['MANO DE OBRA'] = workers_df['MANO DE OBRA']

        # Tools
        works_df['HERRAMIENTAS'] = self.pma_df['HERRAMIENTAS']
        
        for equip, work in special_works_keys.items():
            locator = self.pma_df['DESCRIPCION DEL TRABAJO']\
                    .str.startswith(work['name'])
            length = len(works_df.loc[locator, 'HERRAMIENTAS'])
            works_df.loc[locator, 'HERRAMIENTAS'] = [work['tool_key'] for _ in range(length)]


        # Validations
        assert len(list(filter(lambda x: x not in works_df.columns.values, needed_columns))) == 0
        assert set(needed_columns).issubset(works_df.columns.values)
        assert self.validate_place_keys()
        assert self.validate_tools_keys()

        self.works_df = works_df
        print('Works dataset creation done!\n')

# Extra
    def save_works(self, results_name: Path, works_df: pd.DataFrame) -> None:
        print('Saving works...')
        results_name = str(results_name)
        time_format = "%m-%d-%Y %I %M %p"
        timestamp = datetime.now().strftime(time_format)
        with pd.ExcelWriter(f'{results_name[:-5]} {timestamp}.xlsx') as writer:
            works_df.to_excel(writer, sheet_name='PMA'+timestamp)
        print('Works saved!\n')
    
    def update_database(self, database_name: Path, works_list: list) -> None:
        print('Updating database...')
        col = 'Numero de OT'
        ot = 4
        with sqlite3.connect(database_name) as conn:
            c = conn.cursor()
            for work in works_list:
                print(work.id, work.ot)
                c.execute(f"UPDATE {self.TABLE} SET '{col}' = ? WHERE 'index' = ?", (ot, work.id))
            conn.commit()

            res = c.execute(f'SELECT * from {self.TABLE} WHERE "Numero de OT" NOT NULL')
            for r in res.fetchall():
                print(r)
            print([description[0] for description in res.description])
            
        print('Database updated!')
        

    def create_objects(self, works_df: pd.DataFrame) -> list:
        print('Creating work objects...')
        for work in works_df.iloc:
            work_object = PMAWork()
            work_object.id = work.name
            work_object.titulo = work['TITULO']
            work_object.libranza = work['LIBRANZA']
            work_object.ot = work['OT']
            work_object.ubicacion = work['UBICACION']
            work_object.tipo = work['TIPO']
            work_object.clasificacion = work['CLASIFICACION']
            work_object.cuenta = work['CUENTA']
            work_object.prioridad = work['PRIORIDAD']
            work_object.inicio = work['INICIO']
            work_object.duracion = work['DURACION']
            work_object.supervisor = work['SUPERVISOR']
            work_object.mano_de_obra = work['MANO DE OBRA']
            work_object.herramientas = work['HERRAMIENTAS']

            self.work_list.append(work_object)
        print('Works appended to self work list!\n')



def main() -> None:
    PATH = Path(__file__).parent
    db_file = PATH/'database'/'pma.db'
    db_modified = PATH/'database'/'pma_modified.db'
    results_excel_path = PATH/'excel'/'results.xlsx'
    df = PMADataset(db_file)

    # # Add work details
    # df.add_works_to_df(work_details)

    # # Create Works Dataset
    # df.set_works_df()

    # # Saving works
    # df.save_works(results_excel_path, df.works_df)

    # # Creating objects
    # df.create_objects(df.works_df)

    # # Simulate changing ot number
    # for work in df.work_list:
    #     work.ot = '24'

    # # Updating excel
    # df.update_database(db_modified, df.work_list)



if __name__ == '__main__':
    main()
