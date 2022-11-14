import os.path as osPath

import helpers.env_utils as EnvHelper
import helpers.data_utils as DataHelper

# ============================================================================ #

class BaseballDataBank:

    SOURCE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master'
    ROOT_DIR = EnvHelper.get_root_dir()
    SAVE_DIR = osPath.join(ROOT_DIR, 'data', 'baseball_databank', 'downloads')

    
    def __init__(self, 
                 get_contrib: bool = True, 
                 get_core: bool = True,
                 get_upstream: bool = True):
        
        self.get_contrib = get_contrib
        self.get_core = get_core
        self.get_upstream = get_upstream

  # ============================================================================ #       
  
    @property
    def get_contrib(self) -> bool:
        return self._get_contrib
    
    @get_contrib.setter
    def get_contrib(self, val) -> None:  
        self._get_contrib = val


    @property
    def get_core(self) -> bool:
        return self._get_core
    
    @get_core.setter
    def get_core(self, val) -> None:  
        self._get_core = val
        

    @property
    def get_upstream(self) -> bool:
        return self._get_upstream
    
    @get_upstream.setter
    def get_upstream(self, val) -> None:  
        self._get_upstream = val

  # ============================================================================ #
  
    @property
    def config(self) -> dict:
        _configs = DataHelper.get_json(folder=osPath.join(self.ROOT_DIR, 'configs'),
                                       filename = 'baseball_databank')
        return _configs['fileType']
    
    @property
    def contrib_files(self) -> list:
        return self.config['contrib']
    
    @property
    def core_files(self) -> list:
        return self.config['core']
    
    @property
    def upstream_files(self) -> list:
        return self.config['upstream']
    
    @property
    def contrib_urls(self) -> list:
        return [f'{self.SOURCE_URL}/contrib/{f}.csv' for f in self.contrib_files]
  
    @property
    def core_urls(self):
        return [f'{self.SOURCE_URL}/core/{f}.csv' for f in self.core_files]
    
    @property
    def upstream_urls(self):
        return [f'{self.SOURCE_URL}/upstream/{f}.csv' for f in self.upstream_files]

    @property
    def download_urls(self):
        _urls = []
        _urls.extend(self.contrib_files) if self.get_contrib else _urls
        _urls.extend(self.core_files) if self.get_core else _urls
        _urls.extend(self.upstream_files) if self.get_upstream else _urls
        return _urls
    
# ============================================================================ #

    @classmethod
    def download(cls, 
                 get_contrib: bool = True, 
                 get_core: bool = True,
                 get_upstream: bool = True) -> None:
        
        met = cls(get_contrib, get_core, get_upstream)
        
        DataHelper.download_multiple(url_download_list=met.download_urls,
                                     save_dir=met.SAVE_DIR)    
    

# ============================================================================ #
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')
