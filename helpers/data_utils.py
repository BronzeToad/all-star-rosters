
import json
import os

def get_json(path: str, filename: str, print_flag: bool = False) -> dict:


    filepath = f'{os.path.join(path, filename)}.json'

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        if print_flag:
            print(f'Loading json content from {filepath}...')
    except FileNotFoundError:
        raise FileNotFoundError(f'{filepath} does not exist...')
    
    if len(data) < 1:
        raise ValueError(f'No data loaded. {filename}.json is empty...')
    return data


if __name__ == '__main__':
    print('\n\n------------------------------------------------')

    print(os.path.abspath('.'))
