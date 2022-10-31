import requests
import os

class Downloader:
    
    def __init__(self, url: str, location: str = None):
        self.url = url
        self.location = location
    
    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, val):
        self._url = val
        print(f'url: {self._url}')
    
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self, val):
        if val is None:
            val = 'data/downloads'
            print(f'No download location specified. Defaulting to ~/{val}...')
        else:
            print(f'Download location: {val}')
        self._location = val

    @property
    def filename(self):
        _filename = self.url.split('/')[-1]
        if _filename == '':
            _filename = self.url.split('/')[-2]
        return _filename
    
    @property 
    def filepath(self):
        return os.path.join(self.location, self.filename)
    

    def download(self):
        data = requests.get(self.url)
        with open(self.filepath, 'wb') as file:
            file.write(data.content)
        print(f'{self.filename} downloaded successfully to {self.location}')
    


if __name__ == '__main__':
    print('\n\n------------------------------------------------')

    tst = Downloader(url='https://rickastley.com/summerjamz.zip', location='never/gonna/give/you/up')