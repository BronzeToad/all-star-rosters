import json
import os

def get_json(path: str, filename: str, print_flag: bool = False) -> dict:

    filepath = f'{os.path.join(path, filename)}.json'

    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        if print_flag:
            print(f'Getting json content from {filepath}...')
    except FileNotFoundError:
        raise FileNotFoundError(f'{filepath} does not exist...')
    
    return data


if __name__ == '__main__':
    print('\n\n------------------------------------------------')
