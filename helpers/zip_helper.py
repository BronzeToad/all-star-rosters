from zipfile import ZipFile as zippy

import requests


def download_zip(url, path, filename):
    if filename[-4:] != '.zip':
        filename = filename + '.zip'
    zip = requests.get(url)
    with open(f'{path}{filename}', 'wb') as f:
        f.write(zip.content)


def unzip_file(path, filename, extract_location):
    with zippy(f'{path}{filename}') as zip_ref:
        zip_ref.extractall(extract_location)


if __name__ == '__main__':
    print('Executing as standalone script')

    tst = 'blahBlah_blahziperdoot.zip'

    if tst[-4:] == '.zip':
        print('yes')
    else:
        print('no')