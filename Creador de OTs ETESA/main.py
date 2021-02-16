from pathlib import Path

from load_pma import PMADataset
from ot_creator import OTCreator, WorkFile

def main():
    main_path = Path(__file__).parent
    db_file = main_path/'database'/'pma.db'
    results_file = main_path/'results'/'results.xlsx'
    
    pma = PMADataset(db_file)
    pma.add_works_to_df()
    pma.set_works_df()
    pma.save_works(results_file)
    pma.create_objects(pma.works_df)

    python_file = Path(__file__).parent/'results'/'works.py'
    file = WorkFile(python_file)
    
    maximo = OTCreator()
    # Filtrar primero por trabajos sin OT
    # maximo.create_ots(pma.work_list)
    maximo.add_works_to_file(file)


if __name__ == '__main__':
    main()