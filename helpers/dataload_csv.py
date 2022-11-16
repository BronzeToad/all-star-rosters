import google.cloud.storage as gcpStorage
import os.path as osPath

from pathlib import Path as libPath

import helpers.data_utils as DataHelper
import helpers.env_utils as EnvHelper

# ============================================================================ #

class DataLoadCSV:
    
    ROOT_DIR = EnvHelper.get_root_dir()
    GCP_PROJECT = EnvHelper.get_gcp_project()
    GCP_BUCKET = EnvHelper.get_gcp_bucket()
    
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
        if val not in self.valid_data_sources:
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
    def valid_data_sources(self) -> dict:
        return DataHelper.get_data_sources()

    @property
    def gcp_dir(self) -> str:
        return osPath.join(self.GCP_BUCKET, self.data_source)
    
    @property
    def source_filepath(self) -> str:
        _dir = osPath.join(self.ROOT_DIR, self.source_dir)
        if not libPath(_dir).is_dir():
            raise RuntimeError(f'Invalid source directory: {_dir}.')
        _path = osPath.join(_dir, self.filename)
        if not libPath(_path).is_file():
            raise FileNotFoundError(f'{self.filename} not found in ~/{self.source_dir}')
        return _path
            
    @property
    def gcp_filepath(self) -> str:
        return osPath.join(self.gcp_dir, self.filename)

# ============================================================================ #

    @classmethod
    def doot(cls,
             data_source: str, 
             filename: str) -> None:
        
        met = cls(data_source, filename)
        
        client = gcpStorage.Client(project=met.GCP_PROJECT)
        bucket = client.get_bucket(met.GCP_BUCKET)
        blob = bucket.blob(met.gcp_path)
        blob.upload_from_filename(met.source_path)
        print(f'File {met.filename} uploaded to {met.gcp_dir}.')

# ============================================================================ #

if __name__ == '__main__':
    print('\n\n------------------------------------------------')
    