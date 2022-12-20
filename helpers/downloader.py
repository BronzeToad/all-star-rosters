import os.path as osPath
import requests

from pathlib import Path as libPath
from icecream import ic

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper

BREAK = '\n\n------------------------------------------------'

# ============================================================================ #

class Downloader:

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
        self.response = None
        self.content = None
        
# ============================================================================ #

    @staticmethod
    def check_response_status(response: requests.Response, ignore_errors: bool = False) -> bool:
        status_code = response.status_code
        response_text = response.text
        if status_code != 200:
            if ignore_errors:
                print(f'Unable to download content from {response.url}\n.'
                      f'Request failed with status code: {status_code}\n')
                return False
            else:
                raise RuntimeError(f'Request failed with status code {status_code}...\n'
                                   f'Response text: {response_text}\n')
        elif status_code == 200:
            return True
        else:
            raise RuntimeError(f'API request failed for some other reason...\n'
                               f'Response text: {response_text}\n')
    
    
    @staticmethod
    def save_response_content(content: bytes, save_dir: str, filename: str):
        dir = osPath.join(EnvHelper.get_root_dir(), save_dir)
        if not libPath(dir).is_dir():
            raise RuntimeError(f'Invalid save directory: {dir}.')
        filepath = osPath.join(dir, filename)
        with open(filepath, 'w') as f:
            f.write(str(content))
        if libPath(filepath).is_file():
            print(f'{filename} downloaded to ~/{save_dir}')
        else:
            print(f'{filepath} does not exist...')
            
# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source

    @data_source.setter
    def data_source(self, val) -> None:
        if val not in DataHelper.get_data_sources():
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
    def response(self) -> requests.Response:
        return self._response
        
    @response.setter
    def response(self, val) -> None:
        val = requests.get(self.url)
        self._response = val
    
    
    @property
    def content(self) -> bytes:
        return self._content
    
    @content.setter
    def content(self, val) -> None:
        val = self.response.content
        self._content = val

# ============================================================================ #

    @classmethod
    def download(cls,
                 data_source: str,
                 url: str,
                 save_dir: str = None,
                 filename: str = None,
                 ignore_errors: bool = False) -> None:
    
        doot = cls(data_source, url, save_dir, filename, ignore_errors)
        
        if doot.check_response_status(doot.response):
            doot.save_response_content(doot.content, doot.save_dir, doot.filename)
                
# ============================================================================ #

if __name__ == '__main__':
    print(f'{BREAK} Executing as standalone script...')

    data_source = 'baseball_databank'
    url = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/core/AllstarFull.csv'
    
    Downloader.download(data_source, url)
    
    # tst = Downloader(data_source, url)
    # ic(tst.VALID_DATA_SOURCES)
    # ic(tst.data_source)
    # ic(tst.url)
    # ic(tst.save_dir)
    # ic(tst.filename)
    # ic(tst.ignore_errors)
    # ic(tst.response)
    # ic(tst.content)
