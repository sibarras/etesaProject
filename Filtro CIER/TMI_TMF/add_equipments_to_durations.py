from typing import Dict
import pandas as pd

def add_equipments_to_time_pdf(time_pdf_path, equipments_dict: Dict[str, Dict[str, str]]) -> None:
    
    time_df:pd.DataFrame = pd.read_excel(time_pdf_path, sheet_name=['DURATIONS'])['DURATIONS']
    time_df['equipment'] = ['' for _ in range(len(time_df))]

    for year, data in equipments_dict.items():
        for event, equipment in data.items():
            event_condition = time_df['event'] == int(event)
            year_condition = time_df['year'] == int(year)
            time_df.loc[event_condition & year_condition, 'equipment'] = equipment
    
    time_df.to_excel(time_pdf_path, sheet_name='DURATIONS')
