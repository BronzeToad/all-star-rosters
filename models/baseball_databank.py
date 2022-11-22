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
        self.config = None
        self.filenames_contrib = None
        self.filenames_core = None
        self.filenames_upstream = None
        self.download_urls_contrib = None
        self.download_urls_core = None
        self.download_urls_upstream = None
        self.download_urls = None
        self.filenames = None

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
        return self._config
    
    @config.setter
    def config(self, val) -> None:
        _config_file = DataHelper.get_json(folder=osPath.join(self.ROOT_DIR, 'configs'),
                                           filename = 'baseball_databank')
        val = _config_file['fileType']
        self._config = val
    
    
    @property
    def filenames_contrib(self) -> list:
        return self._filenames_contrib
    
    @filenames_contrib.setter
    def filenames_contrib(self, val) -> None:
        val = self.config['contrib']
        self._filenames_contrib = val
    
    
    @property
    def filenames_core(self) -> list:
        return self._filenames_core
    
    @filenames_core.setter
    def filenames_core(self, val) -> None:
        val = self.config['core']
        self._filenames_core = val
    
    
    @property
    def filenames_upstream(self) -> list:
        return self._filenames_upstream
    
    @filenames_upstream.setter
    def filenames_upstream(self, val) -> None:
        val = self.config['upstream']
        self._filenames_upstream = val
        
        
    @property
    def download_urls_contrib(self) -> list:
        return self._download_urls_contrib
    
    @download_urls_contrib.setter
    def download_urls_contrib(self, val) -> None:
        val = [f'{self.SOURCE_URL}/contrib/{f}.csv' for f in self.filenames_contrib]
        self._download_urls_contrib = val
        
  
    @property
    def download_urls_core(self) -> list:
        return self._download_urls_core
        
    @download_urls_core.setter
    def download_urls_core(self, val) -> None:
        val = [f'{self.SOURCE_URL}/core/{f}.csv' for f in self.filenames_core]
        self._download_urls_core = val
        
    
    @property
    def download_urls_upstream(self) -> list:
        return self._download_urls_upstream
    
    @download_urls_upstream.setter
    def download_urls_upstream(self, val) -> None:
        val = [f'{self.SOURCE_URL}/upstream/{f}.csv' for f in self.filenames_upstream]
        self._download_urls_upstream = val


    @property
    def download_urls(self) -> list:
        return self._download_urls
        
    @download_urls.setter
    def download_urls(self, val) -> None:
        val = []
        val.extend(self.download_urls_contrib) if self.include_contrib else val
        val.extend(self.download_urls_core) if self.include_core else val
        val.extend(self.download_urls_upstream) if self.include_upstream else val
        self._download_urls = val
        
    
    @property
    def filenames(self) -> list:
        return self._filenames
    
    @filenames.setter
    def filenames(self, val) -> None:
        val = []
        val.extend(self.filenames_contrib) if self.include_contrib else val
        val.extend(self.filenames_core) if self.include_core else val
        val.extend(self.filenames_upstream) if self.include_upstream else val
        self._filenames = val
    
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
