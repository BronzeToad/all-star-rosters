import os.path as osPath
import helpers.env_utils as EnvHelper
import helpers.data_utils as DataHelper

import icecream as ic

# ============================================================================ #

class BaseballDataBank:

    BASE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master'
    ROOT_DIR = EnvHelper.get_root_dir()
    CONFIG_DIR = osPath.join(ROOT_DIR, 'configs')
    SAVE_DIR = osPath.join(ROOT_DIR, 'data/baseball_databank/downloads')
    FILENAME_DICT = DataHelper.get_json(CONFIG_DIR, 'baseball_databank')
    
    def __init__(self, **kwargs):
        
        params = {
            'contrib_files': None,
            'core_files': None,
            'upstream_files': None,
        }
        
        params.update(kwargs)
        
        self.contrib_files = params['contrib_files']
        self.core_files = params['core_files']
        self.upstream_files = params['upstream_files']

  # ============================================================================ #       
  
    @property
    def contrib_files(self) -> list:
        return self._contrib_files
    
    @contrib_files.setter
    def contrib_files(self, val) -> None:
        if val is None:
            val = self.FILENAME_DICT['fileType']['contrib']      
        self._contrib_files = val


    @property
    def core_files(self) -> list:
        return self._core_files
    
    @core_files.setter
    def core_files(self, val) -> None:
        if val is None:
            val = self.FILENAME_DICT['fileType']['core']      
        self._core_files = val
        
        
    @property
    def upstream_files(self) -> list:
        return self._upstream_files
    
    @upstream_files.setter
    def upstream_files(self, val) -> None:
        if val is None:
            val = self.FILENAME_DICT['fileType']['upstream']      
        self._upstream_files = val

  # ============================================================================ #
  
    @property
    def contrib_urls(self) -> list:
        return [f'{self.BASE_URL}/contrib/{f}.csv' for f in self.contrib_files]
  
    @property
    def core_urls(self):
        return [f'{self.BASE_URL}/core/{f}.csv' for f in self.core_files]
    
    @property
    def upstream_urls(self):
        return [f'{self.BASE_URL}/upstream/{f}.csv' for f in self.upstream_files]

    @property
    def download_urls(self):
        _urls = []
        for url in [self.contrib_urls, self.core_urls, self.upstream_urls]:
            _urls.extend(url)
        return _urls
    
# ============================================================================ #

    @classmethod
    def download(cls, **kwargs) -> None:
        _cls = cls(**kwargs)
        
        _success = 0
        for url in _cls.download_urls:
            _get = DataHelper.download(url,
                                       location=_cls.SAVE_DIR,
                                       filename=DataHelper.get_filename_from_url(url))
            
            _success += 1 if _get else _success
            
        print(f'{_success} of {len(_cls.download_urls)} data files downloaded successfully to: {_cls.SAVE_DIR}')
        
        

# ============================================================================ #
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')

    BaseballDataBank.download()
    