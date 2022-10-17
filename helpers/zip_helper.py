from zipfile import ZipFile

import requests


class ZipHelper:
    def __init__(self, download_url: str, folder: str, filename: str = None, extract_loc: str = None):
        self.download_url = download_url
        self.folder = folder
        self.filename = filename
        self.extract_loc = extract_loc
        
        
    def get_folder(self):
        if self.folder[-1] != '/':
            self.folder = self.folder + '/'
            
        print(f'folder: {self.folder}')
            
        
    def get_filename(self):
        if self.filename is None:
            self.filename = self.download_url.split('/')[-1]
            
        if self.filename[-4] != '.zip':
            self.filename = self.filename + '.zip'
        
        print(f'filename: {self.filename}')
    
    
    def download_zip(self):
        filepath = f'{self.folder}{self.filename}'
        zip = requests.get(self.download_url)
        with open(filepath, 'wb') as f:
            f.write(zip.content)

        print(f'zip filepath: {filepath}')
        

    def extract_zip(self):
        if self.extract_loc is None:
            self.extract_loc = self.folder
        
        filepath = f'{self.extract_loc}{self.filename}'
        
        with ZipFile(filepath) as zip_ref:
            zip_ref.extractcall(self.extract_loc)
            
        print(f'extract filepath: {filepath}')


    def get_zip(self):
        self.get_folder()
        self.get_filename()
        self.download_zip()
        self.extract_zip()


if __name__ == '__main__':
    print('Executing as standalone script')
