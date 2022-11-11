import os.path as osPath
from dotenv import dotenv_values as dotenvVals
from pathlib import Path as libPath

# ============================================================================ #

def get_env_file() -> str:
    return osPath.join(libPath(__file__).parent.parent, '.env')


def get_env_vars(env_file: str = None) -> dict:
    env_file = get_env_file() if env_file is None else env_file
    if not libPath(env_file).is_file():
        raise FileNotFoundError(f'Unable to locate .env file: {env_file}')
    return dotenvVals(env_file)

# ============================================================================ #

def get_root_dir(env_file: str = None) -> str:
    env_vars = get_env_vars(env_file)
    return env_vars['WORKSPACE_DIR']


def get_env_var(key: str, env_file: str = None) -> str:
    env_vars = get_env_vars(env_file)
    if key not in env_vars:
        raise KeyError(f'Could not find environment variable {key} in .env file...')
    return env_vars[key]

# ============================================================================ #

if __name__ == '__main__':
    print('\n\n-------------------------- Executing as standalone script...')
    