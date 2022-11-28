import google.cloud.storage as gcpStorage
import os.path as osPath

from pathlib import Path as libPath

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper

from icecream import ic

# ============================================================================ #

class DataLoadCSV:
    
    ROOT_DIR = EnvHelper.get_root_dir()
    GCP_PROJECT = EnvHelper.get_gcp_project()
    GCP_BUCKET = EnvHelper.get_gcp_bucket()
    VALID_DATA_SOURCES = DataHelper.get_data_sources()

# ============================================================================ #
    
    def __init__(self, 
                 data_source: str,
                 filename: str,
                 source_dir: str = None):
        
        self.data_source = data_source
        self.filename = filename
        self.source_dir = source_dir
        
# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source

    @data_source.setter
    def data_source(self, val) -> None:
        if val not in self.VALID_DATA_SOURCES:
            raise ValueError(f'Invalid data source: {val}')
        self._data_source = val
        
    
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, val) -> None:
        val = DataHelper.force_extension(val, 'csv')
        self._filename = val
        
    @property
    def source_dir(self) -> str:
        return self._source_dir
    
    @source_dir.setter
    def source_dir(self, val) -> None:
        if val is None:
            val = osPath.join('data', self.data_source)
        self._source_dir = val
        
# ============================================================================ #

    @property
    def gcp_dir(self) -> str:
        return osPath.join(self.GCP_BUCKET, self.data_source)
    
    @property
    def gcp_filepath(self) -> str:
        return osPath.join(self.gcp_dir, self.filename)
    
    @property
    def source_filepath(self) -> str:
        _dir = osPath.join(self.ROOT_DIR, self.source_dir)
        if not libPath(_dir).is_dir():
            raise RuntimeError(f'Invalid source directory: {_dir}.')
        _path = osPath.join(_dir, self.filename)
        if not libPath(_path).is_file():
            raise FileNotFoundError(f'{self.filename} not found in ~/{self.source_dir}')
        return _path
            
# ============================================================================ #

    @classmethod
    def doot(cls,
             data_source: str, 
             filename: str) -> None:
        
        thing = cls(data_source, filename)
        
        client = gcpStorage.Client(project=thing.GCP_PROJECT)
        bucket = client.get_bucket(thing.GCP_BUCKET)
        blob = bucket.blob(thing.gcp_path)
        blob.upload_from_filename(thing.source_path)
        print(f'File {thing.filename} uploaded to {thing.gcp_dir}.')

# ============================================================================ #

if __name__ == '__main__':
    print('\n\n------------------------------------------------')

    data_source = 'baseball_databank'
    filename = 'AwardsManagers'
    tst = DataLoadCSV(data_source, filename)
    
    ic(tst.ROOT_DIR)
    ic(tst.GCP_PROJECT)
    ic(tst.GCP_BUCKET)
    ic(tst.VALID_DATA_SOURCES)
    ic(tst.data_source)
    ic(tst.filename)
    ic(tst.source_dir)
    ic(tst.gcp_dir)
    ic(tst.gcp_filepath)
    ic(tst.source_filepath)    