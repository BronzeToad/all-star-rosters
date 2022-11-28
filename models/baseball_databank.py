import os.path as osPath

import helpers.env_utils as EnvHelper
import helpers.data_utils as DataHelper

from helpers.downloader import Downloader
from helpers.dataload_csv import DataLoadCSV

from random import randint as randomInteger

from icecream import ic

# ============================================================================ #

class BaseballDataBank:

    DATA_SOURCE = 'baseball_databank'
    SOURCE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master'
    ROOT_DIR = EnvHelper.get_root_dir()
    
# ============================================================================ #

    config = DataHelper.get_json(folder=osPath.join(ROOT_DIR, 'configs'), 
                                 filename = 'baseball_databank')
    
    valid_filenames = []
    for _item in config:
        _name = _item['fileName']
        valid_filenames.append(_name)
    
    
# ============================================================================ #
    
    def __init__(self, filenames: list = None):
        self.filenames = filenames

    @property
    def filenames(self) -> list:
        return self._filenames
    
    @filenames.setter
    def filenames(self, val) -> None:
        if val is None:
            val = self.valid_filenames
        else:
            val = [val] if isinstance(val, str) else val
            _invalid_filenames = []
            for _name in val:
                if _name not in self.valid_filenames:
                    _invalid_filenames.append(_name)
                    val.remove(_name)
            if len(_invalid_filenames) > 0:
                print(f'Removed {len(_invalid_filenames)} invalid filenames...')
                ic(_invalid_filenames)
        self._filenames = val
        
# ============================================================================ #
    
    @property
    def urls(self) -> list:
        urls = []
        for _name in self.filenames:
            for _item in self.config:
                if _name == _item['fileName']:
                    _type = _item['fileType']
                    if isinstance(_type, list):
                        for t in _type:
                            urls.append(f'{self.SOURCE_URL}/{t}/{_name}.csv')
                    else:
                        urls.append(f'{self.SOURCE_URL}/{_type}/{_name}.csv')
        return urls

# ============================================================================ #

    @classmethod
    def download(cls, filenames: list = None):
        thing = cls(filenames)
        
        for url in thing.urls:
            Downloader.doot(thing.DATA_SOURCE, url, ignore_errors=True)


    @classmethod
    def dataload(cls, filenames: list = None):
        thing = cls(filenames)
        
        for filename in thing.filenames:
            DataLoadCSV.doot(thing.DATA_SOURCE, filename)

# ============================================================================ #
        
if __name__ == '__main__':
    print('\n\n------------------------------------------------')

    tst = BaseballDataBank()
    ic(tst.DATA_SOURCE)
    # ic(tst.SOURCE_URL)
    # ic(tst.ROOT_DIR)
    # ic(tst.config)
    # ic(tst.valid_filenames)
    ic(tst.filenames)
    ic(tst.urls)