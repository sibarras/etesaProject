import pandas as pd
from pathlib import Path

def read_works_excel(excel_file: Path):
    assert excel_file.is_file() and excel_file.name.endswith('.xlsx')
    ans_df: pd.DataFrame = pd.read_excel(excel_file, header=1, usecols=range(0,22))
    return ans_df

def export_data_to_excel(data_df: pd.DataFrame, file: Path) -> None:
    assert file.parent.exists() and file.parent.is_dir()
    data_df.to_excel(file, 'results')