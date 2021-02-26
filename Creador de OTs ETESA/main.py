from pathlib import Path
import pandas as pd

from load_pma import PMADataset
from ot_creator import OTCreator, WorkFile
from works_struc import PMAWork

# Esta es para pruebas solamente de uno o dos trabajos
from works_example import works

def main():
    # Determino las rutas de los archivos
    main_path = Path(__file__).parent
    db_file = main_path/'database'/'pma.db'
    results_file = main_path/'results'/'results.xlsx'
    excel_pma_file = main_path/'excel'/'PMA2021_Pruebas_Y_Mediciones_VF.xlsx'
    ot_txt_folder = main_path/'ots'
    
    # Creo el PMA cargando la base de datos
    pma = PMADataset(db_file)
    # Creo el dataframe
    pma.add_works_to_df()
    # Formateo el dataframe para que sea lo que necesita el maximo
    pma.set_works_df()
    # Guardo los resultados en un excel

    filtered_works = pma.works_df.loc[
        (pma.pma_df['MES'] != 'ENERO').to_numpy()
        & ~pma.works_df['OT'].notnull()]
    
    print(filtered_works)
    
    pma.create_objects(filtered_works)

    python_file = Path(__file__).parent/'results'/'works.py'
    file = WorkFile(python_file)
    
    maximo = OTCreator(file, excel_pma_file)
    maximo.ot_folder = ot_txt_folder
    maximo.create_ots(pma.work_list)
    pma.save_works(results_file, maximo.get_works_dataframe())


if __name__ == '__main__':
    main()