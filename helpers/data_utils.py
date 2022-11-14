import json
import requests
import os.path as osPath
from pathlib import Path as libPath


def force_extension(filename: str, extension: str) -> str:
    ext = libPath(filename).suffix
    if ext == '':
        filename = f'{filename}.{extension}'
    elif ext != extension:
        raise ValueError(f'Invalid filename extension {ext}. Expected {extension}.')
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


def download(url: str, save_dir: str, filename: str) -> None:
    filepath = osPath.join(save_dir, filename)
    payload = requests.get(url)
    status_code = payload.response.status_code
    
    if status_code != 200:
        raise RuntimeError(f'Request failed with status code {status_code}...\n'
                           f'Response text: {payload.response.text}')
    
    with open(filepath, 'wb') as file:
        file.write(payload.content)
    
    if libPath(filepath).is_file():
        print(f'{filename} downloaded to {save_dir}.')
    else:
        raise FileNotFoundError(f'{filepath} does not exist..')


def download_multiple(url_download_list: list, save_dir: str) -> None:

    for url in url_download_list:
        filename = get_filename_from_url(url)
        filepath = osPath.join(save_dir, filename)
        payload = requests.get(url)
        status_code = payload.response.status_code
        
        if status_code != 200:
            print(f'Unable to download {filename} from {url}. Request failed with status code: {status_code}')
            pass
        else:
            with open(filepath, 'wb') as file:
                file.write(payload.content)

        if libPath(filepath).is_file():
            print(f'{filename} downloaded to {save_dir}.')


if __name__ == '__main__':
    print('\n\n------------------------------------------------')


    url = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/notReal.csv'
    filename = 'notReal.csv'
    save_dir = 'data'
    
    print(download(url, save_dir, filename))