import json
import requests
import os.path as osPath
from pathlib import Path as libPath


def force_extension(filename: str, extension: str) -> str:
    _ext = libPath(filename).suffix
    if _ext == '':
        filename = f'{filename}.{extension}'
    elif _ext != extension:
        raise ValueError(f'Invalid filename extension {_ext}. Expected {extension}.')
    return filename


def get_json(folder: str, filename: str) -> dict:
    """Gets json file and loads contents into a dictionary object.
    Parameters
    ----------
    folder : str
        Path to directory containing json file.
    filename : str
        Name of json file to be loaded.
    Returns
    -------
    _data : dict
        Contents of json file as a python dictionary object.
    Raises
    ------
    ValueError
        If filename extension is something other than null or 'json'.
    FileNotFoundError
        If json file can't be found.
    ValueError
        If contents of json file are empty.
    """
    
    _filename = force_extension(filename, 'json')
    _filepath = f'{osPath.join(folder, _filename)}'

    if libPath(_filepath).is_file():
        with open(_filepath, 'r') as file:
            _data = json.load(file)
    else:
        raise FileNotFoundError(f'File {_filename} not found in {folder}.')
    
    if len(_data) < 1:
        raise ValueError(f'No data loaded. {_filename} is empty...')
    
    return _data


def get_filename_from_url(url: str) -> str:
    _name = url.split('/')[-1]
    return url.split('/')[-2] if _name == '' else _name


def download(url: str, location: str, filename: str) -> bool:
    _filepath = osPath.join(location, filename)
    _payload = requests.get(url)
    
    with open(_filepath, 'wb') as file:
        file.write(_payload.content)

    return libPath(_filepath).is_file() 



if __name__ == '__main__':
    print('\n\n------------------------------------------------')
