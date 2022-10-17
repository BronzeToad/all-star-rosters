import requests
import os
    

def download_from_url(url: str, folder: str = None, filename: str = None):
    if folder is None:
        folder = 'data/downloads'
    print(f'folder: {folder}')
    
    if filename is None:
        filename = url.split('/')[-1]
        if filename == '':
            filename = url.split('/')[-2]
    print(f'filename: {filename}')
        
    filepath = os.path.join(folder, filename)
    
    data = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(data.content)
    
    print(f'file from url downloaded successfully to: {filepath}')


if __name__ == '__main__':
    print('Executing as standalone script')

    tst_url = 'https://raw.githubusercontent.com/BronzeToad/baseballdatabank/master/core/AllstarFull.csv'
    download_from_url(tst_url)