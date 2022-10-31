import helpers.data_utils as DataHelper
from models.data_extractor import DataExtractor


class BaseballDataBank(DataExtractor):
    BASE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/'
    
    def __init__(self, download_url, location, filename, filetype, filepath,
                 contrib_files: list = None,
                 core_files: list = None,
                 upstream_files: list = None):
        
        super().__init__(download_url, location, filename, filetype, filepath)
        
        self.contrib_files = contrib_files
        self.core_files = core_files
        self.upstream_files = upstream_files
    
    
    @property
    def contrib_files(self):
        return self._contrib_files
    
    @contrib_files.setter
    def contrib_files(self):
        self._contrib_files = []
        print(f'contrib_files: {self._contrib_files}')


    @property
    def core_files(self):
        return self._core_files
    
    @core_files.setter
    def core_files(self, val):
        self._core_files = val
        print(f'core_files: {self._core_files}')
        
        
    @property
    def upstream_files(self):
        return self._upstream_files
    
    @upstream_files.setter
    def upstream_files(self, val):
        self._upstream_files = val
        print(f'upstream_files: {self._upstream_files}')
        
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')
    
    def print_sys_paths():
        import sys
        for p in sys.path:
            print(p)
            
    
    print_sys_paths()