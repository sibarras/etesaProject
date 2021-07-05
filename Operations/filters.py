import pandas as pd

def split_operation_steps(operation_steps: str) -> pd.Series:
    if pd.isna(operation_steps):
        return pd.Series({}, name='operations', dtype='string')

    lines_split_list = operation_steps.splitlines()
    def lines_filter(line: str):
        if len(line) != 0:
            return line[0].isnumeric()
        return False

    filtered_list = list(filter(lines_filter, lines_split_list))
    operations_dict = {int(operation[0]): operation[4:].strip() for operation in filtered_list}
    return pd.Series(operations_dict, name='operations', dtype='string')


def change_operations_to_df(work_operations: pd.Series) -> pd.DataFrame:
    '''Get a series of operation steps and returns a dataframe with the data.'''

    re_dict: dict[str, str] = {
        'Equipos': r'([0-9]{1,2}[a-zA-Z]{1,2}[0-9]{1,3})',
        'Líneas': r'([0-9]{1,4}-[0-9a-zA-Z]{1,4})',
        'Subestaciones': r'(?:S\/E|[Ss][Uu][Bb][Ee][Ss][Tt][Aa][Cc][Ii][Ooó][Nn]) (?:(?:LLANO \w+)|(?:SAN \w+)|(?:MATA DE \w+)|(?:SANTA \w+)|(?:PANAM[AÁ] [2I]{2})|\w+)'
    }

    data_dict = {name: work_operations.str.findall(re) for name, re in re_dict.items()}
    return pd.DataFrame(data_dict)

