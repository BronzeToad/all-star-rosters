import json
import os.path as osPath

from datetime import datetime
from dateutil.parser import parse as dateutilParse
from pathlib import Path as libPath
from string import capwords as strCapwords

import helpers.env_utils as EnvHelper

# ============================================================================ #

ROOT_DIR = EnvHelper.get_root_dir()

# ============================================================================ #

def force_extension(filename: str, extension: str) -> str:
    ext = libPath(filename).suffix
    if ext == '':
        filename = f'{filename}.{extension}'
    elif ext != extension:
        raise ValueError(f'Invalid filename extension {ext}. Expected {extension}.')
    return filename


def get_json(folder: str, filename: str) -> dict:   
    filename = force_extension(filename, 'json')
    filepath = f'{osPath.join(folder, filename)}'

    if libPath(filepath).is_file():
        with open(filepath, 'r') as file:
            data = json.load(file)
    else:
        raise FileNotFoundError(f'{filename} not found in {folder}.')
    
    if len(data) < 1:
        raise ValueError(f'No data loaded. {filename} is empty...')
    
    return data


def get_filename_from_url(url: str) -> str:
    filename = url.split('/')[-1]
    return url.split('/')[-2] if filename == '' else filename


def get_data_sources() -> list:
    _config = get_json(folder=osPath.join(ROOT_DIR, 'configs'),
                       filename='data_sources')
    return _config['dataSources']


def get_epoch_timestamp(date_string: str = None, fuzzy: bool = False) -> str:
    if date_string is None:
        _val = datetime.now()
    else:
        _val = dateutilParse(date_string, fuzzy=True) if fuzzy else dateutilParse(date_string)
        
    return str(_val.strftime('%s'))


def snek_to_camel(snek_string: str) -> str:
    return strCapwords(snek_string.replace('_', ' ')).replace(' ', '')

# ============================================================================ #

if __name__ == '__main__':
    print('\n\n------------------------------------------------')


    test_date = 'Today'
    
    print(get_epoch_timestamp(test_date, fuzzy=True))