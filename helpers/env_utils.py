from typing import Union
from dotenv import dotenv_values


def get_env_variable(key: str) -> Union[str, None]:
    config = dotenv_values('.env')
    try:
        val = config[key]
    except KeyError:
        print(f'Could not find environment variable {key} in .env file')
        val = None
    finally:
        return val


if __name__ == '__main__':
    print('\n\n------------------------------------------------')
