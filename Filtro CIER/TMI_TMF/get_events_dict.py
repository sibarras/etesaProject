from pathlib import Path
from typing import Dict

def get_event_from_pdf_name(string: str) -> str:
    return string.split('_')[0].lstrip('IE')

def get_events_dict(path:Path) -> dict:
    """Returns Events Dictionary in a folder with folders inside with numeric names.

    Args:
        path (Path): the folder that cointains the numeric named folders. Inside this folders you need to have .pdf events

    Returns:
        dict: returns a dictionary of {filename: fileDict} with filedict: {eventStrNumber: eventStrFilePath}
    """
    events_dict:Dict[str, Dict[str, str]] = {}
    for file in path.iterdir():
        if file.is_dir() and file.name.isnumeric():
            events_dict[file.name] = {}
            for event in file.glob('*.pdf'):
                events_dict[file.name][get_event_from_pdf_name(event.name)] = event.absolute().__str__()
    
    return events_dict
