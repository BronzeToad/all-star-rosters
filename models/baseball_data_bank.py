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
        
