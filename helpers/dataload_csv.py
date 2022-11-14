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
                 filename: str):
        
        self.data_source = data_source
        self.filename = filename
        
# ============================================================================ #

    @property
    def data_source(self) -> str:
        return self._data_source

    @data_source.setter
    def data_source(self, val) -> None:
        self._data_source = val
        
    
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, val) -> None:
        val = DataHelper.force_extension(val, 'csv')
        self._filename = val
        
# ============================================================================ #

    @property
    def config(self) -> dict:
        _configs = DataHelper.get_json(folder=osPath.join(self.ROOT_DIR, 'configs'), 
                                       filename='gcp_storage_configs')
        return _configs[self.data_source]

    @property
    def source_dir(self) -> str:
        return self.config['sourceDirectory']

    @property
    def gcp_dir(self) -> str:
        return self.config['gcpDirectory']
    
    @property
    def source_path(self) -> str:
        _path = osPath.join(self.source_dir, self.filename)
        if libPath(_path).is_file():
            return _path
        else:
            raise FileNotFoundError(f'File {self.filename} not found in {self.source_dir}')

    @property
    def gcp_path(self) -> str:
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
    