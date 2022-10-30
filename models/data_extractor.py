import requests
import os

class DataExtractor:
    
    def __init__(self, 
                 download_url: str, 
                 location: str = 'data/downloads', 
                 filename: str = None,
                 filetype: str = None,
                 filepath: str = None):
        
    # maybe add direct_download flag, api methods
        self.download_url = download_url
        self.location = location
        self.filename = filename
        self.filetype = filetype
        self.filepath = filepath
    
    @property
    def download_url(self):
        return self._download_url
    
    @download_url.setter
    def download_url(self, val):
        self._download_url = val
        print(f'download_url: {self._download_url}')
    
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, val):
        self._location = val
        print(f'location: {self._location}')
        
    
    @property
    def filename(self):
        return self._filename
    
    @filename.setter
    def filename(self, val):
        if val is None:
            val = self.download_url.split('/')[-1].split('.')[0]
            if val == '':
                val = self.download_url.split('/')[-2].split('.')[0]
        self._filename = val
        print(f'filename: {self._filename}')
    
    
    @property
    def filetype(self):
        return self._filetype
    
    @filetype.setter
    def filetype(self, val):
        if val is None:
            val = self.download_url.split('/')[-1].split('.')[-1]
            if val == '':
                val = self.download_url.split('/')[-2].split('.')[-1]
        if len(val) < 3 or len(val) > 4:
            raise ValueError('Invalid file type...probably.')
        self._filetype = val
        print(f'filetype: {self._filetype}')
        
        
    @property 
    def filepath(self):
        return self._filepath
    
    @filepath.setter
    def filepath(self, val):
        if val is None:
            val = os.path.join(self.location, self.filename)
            val = f'{val}.{self.filetype}'
        self._filepath = val
        print(f'filepath: {self._filepath}')
        

    def download(self):
        data = requests.get(self.download_url)
        with open(self.filepath, 'wb') as file:
            file.write(data.content)
        print(f'{self.filename}.{self.filetype} downloaded successfully to {self.location}')
    

if __name__ == '__main__':
    print('\n\n------------------------------------------------')
     
    url = 'https://raw.githubusercontent.com/BronzeToad/baseballdatabank/master/core/AllstarFull.csv'
    tst = DataExtractor(download_url=url)
    
    tst.download()
    