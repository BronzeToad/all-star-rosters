import os.path as osPath

import helpers.env_utils as EnvHelper
import helpers.data_utils as DataHelper

# ============================================================================ #

class BaseballDataBank:

    SOURCE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master'
    ROOT_DIR = EnvHelper.get_root_dir()
    SAVE_DIR = osPath.join(ROOT_DIR, 'data', 'baseball_databank', 'downloads')

    
    def __init__(self, 
                 filetype_contrib: bool = True, 
                 filetype_core: bool = True,
                 filetype_upstream: bool = True):
        
        self.filetype_contrib = filetype_contrib
        self.filetype_core = filetype_core
        self.filetype_upstream = filetype_upstream

  # ============================================================================ #       
  
    @property
    def filetype_contrib(self) -> bool:
        return self._filetype_contrib
    
    @filetype_contrib.setter
    def filetype_contrib(self, val) -> None:  
        self._filetype_contrib = val


    @property
    def filetype_core(self) -> bool:
        return self._filetype_core
    
    @filetype_core.setter
    def filetype_core(self, val) -> None:  
        self._filetype_core = val
        

    @property
    def filetype_upstream(self) -> bool:
        return self._filetype_upstream
    
    @filetype_upstream.setter
    def filetype_upstream(self, val) -> None:  
        self._filetype_upstream = val

  # ============================================================================ #
  
    @property
    def download_config(self) -> dict:
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
    def download_url_contrib(self) -> list:
        return [f'{self.SOURCE_URL}/contrib/{f}.csv' for f in self.filenames_contrib]
  
    @property
    def download_url_core(self):
        return [f'{self.SOURCE_URL}/core/{f}.csv' for f in self.filenames_core]
    
    @property
    def download_url_upstream(self):
        return [f'{self.SOURCE_URL}/upstream/{f}.csv' for f in self.filenames_upstream]

    @property
    def download_urls(self):
        _urls = []
        _urls.extend(self.filenames_contrib) if self.filetype_contrib else _urls
        _urls.extend(self.filenames_core) if self.filetype_core else _urls
        _urls.extend(self.filenames_upstream) if self.filetype_upstream else _urls
        return _urls
    
# ============================================================================ #

    @classmethod
    def download(cls, 
                 filetype_contrib: bool = True, 
                 filetype_core: bool = True,
                 filetype_upstream: bool = True) -> None:
        
        met = cls(filetype_contrib, filetype_core, filetype_upstream)
        
        DataHelper.download_multiple(url_download_list=met.download_urls,
                                     save_dir=met.SAVE_DIR)    
    
    
    @classmethod
    def download(cls, 
                 filetype_contrib: bool = True, 
                 filetype_core: bool = True,
                 filetype_upstream: bool = True) -> None: pass
        

# ============================================================================ #
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')
