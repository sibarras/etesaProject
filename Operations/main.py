import pandas as pd
from functools import reduce

from excel_handler import (
    read_works_excel, Path,
    export_data_to_excel,
)

from filters import (
    split_operation_steps,
    change_operations_to_df,
)

def main():
    # Define path for files
    MAIN_PATH = Path(__file__).parent
    works_excel_file =  MAIN_PATH/'excel'/'operations'/'libranzas2020.xlsx'
    results_excel_file = MAIN_PATH/'excel'/'results'/works_excel_file.name

    # Define important cols for the program
    work_id = 'Número'
    last_state_col = 'Último Estado'
    start_date_col = 'Fecha Inicio'
    end_date_col = 'Fecha Final'
    initial_operations_col = 'Maniobras de Iniciación'
    final_operations_col = 'Maniobras de Finalización'
    agent = 'Agente'

    operation_cols = [ initial_operations_col, final_operations_col ]
    time_cols = [ start_date_col, end_date_col ]
    
    important_cols = [
        work_id, last_state_col, *time_cols, *operation_cols,
    ]

    # Get the dataframe from excel file
    works_df = read_works_excel(works_excel_file)

    # Filter works deleting rejected or cancelled
    works_completed_df = works_df.loc[
        ( works_df[last_state_col] != 'Cancelado' )
        & ( works_df[last_state_col] != 'Rechazado' )
        & ( works_df[agent] == 'ETESA' )
    ]

    # Take only important columns for each work
    important_data_df: pd.DataFrame = works_completed_df.loc[:, important_cols]

    # Organize the operations in each work, separating them by steps in series
    operations_splitted_df = important_data_df[operation_cols].applymap(split_operation_steps)

    # Take the operation series and returns a dataframe with operations info
    operations_with_elements_df = operations_splitted_df.applymap(change_operations_to_df)

    # Falta Poner uniformidad en los datos para asi poder saber en un dia de tabajo la cantidad de veces que se uso algo y donde

    # Take other important information to put inside the use
    for col, time in zip(operation_cols, time_cols):
        for work in important_data_df.iloc:
            additional_values_dict = {
                'Fecha': important_data_df[time][work.name],
                'Libranza': important_data_df[work_id][work.name],
                'Tipo de Maniobra': col,
            }
            operations_with_elements_df.loc[:, col][work.name]['Fecha'] = additional_values_dict['Fecha']
            operations_with_elements_df.loc[:, col][work.name]['Libranza'] = additional_values_dict['Libranza']
            operations_with_elements_df.loc[:, col][work.name]['Tipo de Maniobra'] = additional_values_dict['Tipo de Maniobra']

    # Flat the information in a single dataframe
    operations_df = reduce(lambda acc, el: operations_with_elements_df[acc].append(operations_with_elements_df[el], ignore_index=True), operation_cols)
    operations_df: pd.DataFrame = reduce(lambda acc, el: acc.append(el, ignore_index=True), operations_df.iloc)
    operations_df = operations_df.sort_values('Fecha')

    # Save data to excel
    export_data_to_excel(operations_df, results_excel_file)

if __name__ == "__main__":
    main()