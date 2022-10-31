import os

import helpers.data_utils as DataHelper
from models.data_extracts import Downloader

ROOT_DIR = os.getenv("ROOT_DIR")

class BaseballDataBank(Downloader):
    BASE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master'
    
    def __init__(self, url: str, location: str = None):
        super().__init__(url, location)
  
    @property
    def config(self):
        return DataHelper.get_json(f'{ROOT_DIR}/configs', 'mlb_data_bank')
  
    @property
    def contrib_files(self):
        return self.config['dataType']['contrib']
    
    @property
    def core_files(self):
        return self.config['dataType']['core']
    
    @property
    def upstream_files(self):
        return self.config['dataType']['upstream']

    @property
    def url_list(self):
        _url_list = []
        [_url_list.append(f'{self.BASE_URL}/contrib/{f}.csv') for f in self.contrib_files]
        [_url_list.append(f'{self.BASE_URL}/core/{f}.csv') for f in self.core_files]
        [_url_list.append(f'{self.BASE_URL}/upstream/{f}.csv') for f in self.upstream_files]
        return _url_list
    
    '''     FIXME
    def get_data(self):
        if len(self.url_list) == 0:
            self.get_urls()
        for url in self.url_list:
            DataHelper.download_from_url(url=url, folder='data/baseball_databank')
    '''
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')
    

    tst = BaseballDataBank(url='https://rickastley.com/summerjamz.zip')


    for url in tst.url_list:
        print(url)
    

