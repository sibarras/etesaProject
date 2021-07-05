from os import mkdir
from pathlib import Path
from typing import Dict

output_path = Path(__file__).parent / 'txt'
if not output_path.exists():
    mkdir(output_path)

def make_events_txt(name:str, event_dict: Dict[str, Dict[str, str]]) -> None:
    
    if not (output_path/name).exists(): mkdir(output_path/name)

    for year, events in event_dict.items():
        # Add .txt if doesnt have it in the name
        txt_name = f'{name}_{year}.txt' if name.find('.txt')==-1 else f'{name}_{year}'
        txt_path = output_path / name / txt_name
        with open(txt_path, 'wt') as f:
            for event_num, info in events.items():
                f.write(event_num+':\n')
                f.write('\t'+info+'\n\n')

