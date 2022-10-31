import helpers.data_utils as DataHelper
from models.data_extracts import Downloader


class BaseballDataBank(Downloader):
    BASE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/'
    
    def __init__(self, url, location,

                 contrib_files: list = None,
                 core_files: list = None,
                 upstream_files: list = None):
        
        Downloader.__init__(url, location)
        
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

                 data_type: str = None):
        
        super().__init__(download_url, location, filename, filetype, filepath)
        
        self.data_type = data_type
    
    
    @property
    def data_type(self):
        return self._data_type
    
    @data_type.setter
    def data_type(self, val):
        self._data_type = val
        print(f'data_type: {self._data_type}')

 
    @property
    def url_list(self):
        return self._url_list
    
    @url_list.setter
    def url_list(self, val):
        self._url_list = val
        print(f'url_list: {self._url_list}')
        
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')
    

    def print_sys_paths():
        import sys
        for p in sys.path:
            print(p)
            
    
    print_sys_paths()


    
    

