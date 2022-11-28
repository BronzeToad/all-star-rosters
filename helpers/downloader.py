import os.path as osPath
import requests

from pathlib import Path as libPath
from icecream import ic

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper

from icecream import ic

# ============================================================================ #

class Downloader:
    
    ROOT_DIR = EnvHelper.get_root_dir()
    VALID_DATA_SOURCES = DataHelper.get_data_sources()
    
# ============================================================================ #
    
    def __init__(self,
                 data_source: str,
                 url: str,
                 save_dir: str = None,
                 filename: str = None,
                 ignore_errors: bool = False):
        
        self.data_source = data_source
        self.url = url
        self.save_dir = save_dir
        self.filename = filename
        self.ignore_errors = ignore_errors
        self.payload = None
        self.payload_content = None
        self.status_code = None

# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source

    @data_source.setter
    def data_source(self, val) -> None:
        if val not in self.VALID_DATA_SOURCES:
            raise ValueError(f'Invalid data source: {val}')
        self._data_source = val
        

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, val: str) -> None:
        self._url = val


    @property
    def save_dir(self) -> str:
        return self._save_dir
    
    @save_dir.setter
    def save_dir(self, val: str) -> None:
        if val is None:
            val = osPath.join('data', self.data_source)
        self._save_dir = val


    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, val: str) -> None:
        if val is None:
            val = DataHelper.get_filename_from_url(self.url)
        self._filename = val


    @property
    def ignore_errors(self) -> bool:
        return self._ignore_errors
    
    @ignore_errors.setter
    def ignore_errors(self, val: bool) -> None:
        self._ignore_errors = val

# ============================================================================ #

    @property
    def save_filepath(self) -> str:
        _dir = osPath.join(self.ROOT_DIR, self.save_dir)
        if not libPath(_dir).is_dir():
            raise RuntimeError(f'Invalid save directory: {_dir}.')
        return osPath.join(_dir, self.filename)


    @property
    def payload(self) -> requests.Response:
        return self._payload
        
    @payload.setter
    def payload(self, val) -> None:
        val = requests.get(self.url)
        self._payload = val
    
    @property
    def payload_content(self) -> bytes:
        return self._payload_content
        
    @payload_content.setter
    def payload_content(self, val) -> None:
        val = self.payload.content
        self._payload_content = val
    
    @property
    def status_code(self) -> int:
        return self._status_code
        
    @status_code.setter
    def status_code(self, val) -> None:
        val = self.payload.status_code
        self._status_code = val
        
# ============================================================================ #

    @classmethod
    def doot(cls,
             data_source: str,
             url: str,
             save_dir: str = None,
             filename: str = None,
             ignore_errors: bool = False) -> None:
    
        thing = cls(data_source, url, save_dir, filename, ignore_errors)
    
        if thing.status_code != 200:
            if thing.ignore_errors:
                print(f'Unable to download {thing.filename} from {thing.url}.' 
                      f'Request failed with status code: {thing.status_code}')
            else:
                raise RuntimeError(f'Request failed with status code {thing.status_code}...\n'
                                   f'Response text: {thing.payload.text}.')
        else:
            with open(thing.save_filepath, 'wb') as file:
                file.write(thing.payload_content)
        
        if libPath(thing.save_filepath).is_file():
            print(f'{thing.filename} downloaded to ~/{thing.save_dir}.')
        elif not thing.ignore_errors:
            raise FileNotFoundError(f'{thing.save_filepath} does not exist..')
                
# ============================================================================ #

if __name__ == '__main__':
    print('\n\n------------------------------------------------')

    data_source = 'baseball_databank'
    url = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/AllstarFull.csv'
    tst = Downloader(data_source, url)
    
    # ic(tst.ROOT_DIR)
    # ic(tst.VALID_DATA_SOURCES)
    ic(tst.data_source)
    ic(tst.url)
    ic(tst.save_dir)
    ic(tst.filename)
    ic(tst.ignore_errors)
    ic(tst.payload)
    # ic(tst.payload_content)
    # ic(tst.status_code)
    