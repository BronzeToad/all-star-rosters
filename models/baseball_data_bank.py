from models.data_extractor import DataExtractor

class BaseballDataBank(DataExtractor):
    BASE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/'
    
    def __init__(self, download_url, location, filename, filetype, filepath,
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
    

    
    