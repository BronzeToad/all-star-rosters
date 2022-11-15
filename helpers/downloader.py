import os.path as osPath
import requests

from pathlib import Path as libPath

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper

# ============================================================================ #

class Downloader:
    
    ROOT_DIR = EnvHelper.get_root_dir()
    
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

# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source

    @data_source.setter
    def data_source(self, val) -> None:
        if val not in self.valid_data_sources:
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


    @property
    def payload(self):
        return self._payload
    
    @payload.setter
    def payload(self, val) -> None:
        self._payload = val
        
    @property
    def response(self):
        return self._response
    
    @response.setter
    def response(self, val) -> None:
        self._response = val

# ============================================================================ #

    @property
    def save_filepath(self) -> str:
        _dir = osPath.join(self.ROOT_DIR, self.save_dir)
        if not libPath(_dir).is_dir():
            raise RuntimeError(f'Invalid save directory: {_dir}.')
        return osPath.join(_dir, self.filename)

    @property
    def valid_data_sources(self) -> dict:
        return DataHelper.get_data_sources()

    @property
    def payload(self) -> requests.Response:
        return requests.get(self.url)
    
    @property
    def payload_content(self) -> bytes:
        return self.payload.content
    
    @property
    def status_code(self) -> int:
        return self.payload.status_code


# ============================================================================ #\

    @classmethod
    def doot(cls,
             data_source: str,
             url: str,
             save_dir: str = None,
             filename: str = None,
             ignore_errors: bool = False) -> None:
    
        met = cls(data_source, url, save_dir, filename, ignore_errors)
    
        if met.status_code != 200:
            if met.ignore_errors:
                print(f'Unable to download {met.filename} from {met.url}.' 
                      f'Request failed with status code: {met.status_code}')
            else:
                raise RuntimeError(f'Request failed with status code {met.status_code}...\n'
                                   f'Response text: {met.payload.text}.')
        else:
            with open(met.save_filepath, 'wb') as file:
                file.write(met.payload_content)
        
        if libPath(met.save_filepath).is_file():
            print(f'{met.filename} downloaded to ~/{met.save_dir}.')
        elif not met.ignore_errors:
            raise FileNotFoundError(f'{met.save_filepath} does not exist..')
                

# ============================================================================ #

if __name__ == '__main__':
    print('\n\n------------------------------------------------')
