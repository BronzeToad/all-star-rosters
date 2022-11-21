import os.path as osPath

import helpers.env_utils as EnvHelper
import helpers.data_utils as DataHelper

from helpers.downloader import Downloader
from helpers.dataload_csv import DataLoadCSV

# ============================================================================ #

class BaseballDataBank:

    DATA_SOURCE = 'baseball_databank'
    SOURCE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master'
    ROOT_DIR = EnvHelper.get_root_dir()

    def __init__(self, 
                 include_contrib: bool = True, 
                 include_core: bool = True,
                 include_upstream: bool = True):
        
        self.include_contrib = include_contrib
        self.include_core = include_core
        self.include_upstream = include_upstream

  # ============================================================================ #       
  
    @property
    def include_contrib(self) -> bool:
        return self._include_contrib
    
    @include_contrib.setter
    def include_contrib(self, val) -> None:  
        self._include_contrib = val


    @property
    def include_core(self) -> bool:
        return self._include_core
    
    @include_core.setter
    def include_core(self, val) -> None:  
        self._include_core = val
        

    @property
    def include_upstream(self) -> bool:
        return self._include_upstream
    
    @include_upstream.setter
    def include_upstream(self, val) -> None:  
        self._include_upstream = val

  # ============================================================================ #
  
    @property
    def config(self) -> dict:
        _configs = DataHelper.get_json(folder=osPath.join(self.ROOT_DIR, 'configs'),
                                       filename = 'baseball_databank')
        return _configs['fileType']
    
    @property
    def filenames_contrib(self) -> list:
        return self.config['contrib']
    
    @property
    def filenames_core(self) -> list:
        return self.config['core']
    
    @property
    def filenames_upstream(self) -> list:
        return self.config['upstream']
    
    @property
    def download_urls_contrib(self) -> list:
        return [f'{self.SOURCE_URL}/contrib/{f}.csv' for f in self.filenames_contrib]
  
    @property
    def download_urls_core(self) -> list:
        return [f'{self.SOURCE_URL}/core/{f}.csv' for f in self.filenames_core]
    
    @property
    def download_urls_upstream(self) -> list:
        return [f'{self.SOURCE_URL}/upstream/{f}.csv' for f in self.filenames_upstream]

    @property
    def download_urls(self) -> list:
        _urls = []
        _urls.extend(self.download_urls_contrib) if self.include_contrib else _urls
        _urls.extend(self.download_urls_core) if self.include_core else _urls
        _urls.extend(self.download_urls_upstream) if self.include_upstream else _urls
        return _urls
    
    @property
    def filenames(self) -> list:
        _names = []
        _names.extend(self.filenames_contrib) if self.include_contrib else _names
        _names.extend(self.filenames_core) if self.include_core else _names
        _names.extend(self.filenames_upstream) if self.include_upstream else _names
        return _names
    
# ============================================================================ #

    @classmethod
    def download(cls, 
                 include_contrib: bool = True, 
                 include_core: bool = True,
                 include_upstream: bool = True) -> None:
        
        met = cls(include_contrib, include_core, include_upstream)
        
        for url in met.download_urls:
            Downloader.doot(met.DATA_SOURCE, url, ignore_errors=True)


    @classmethod
    def dataload(cls, 
                 include_contrib: bool = True, 
                 include_core: bool = True,
                 include_upstream: bool = True) -> None:
        
        met = cls(include_contrib, include_core, include_upstream)
        
        for filename in met.filenames:
            DataLoadCSV.doot(met.DATA_SOURCE, filename)
        

# ============================================================================ #
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')
