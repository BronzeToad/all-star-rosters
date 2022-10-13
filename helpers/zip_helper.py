import requests
from zipfile import ZipFile as zippy


def download_zip(url, path, filename):
    zip = requests.get(url)
    with open(f'{path}{filename}', 'wb') as f:
        f.write(zip.content)


def unzip_file(path, filename, extract_location):
    with zippy(f'{path}{filename}') as zip_ref:
        zip_ref.extractall(extract_location)


if __name__ == '__main__':
    print('Executing as standalone script')

    url = 'https://www.retrosheet.org/gamelogs/gl1871.zip'
    path = 'test_output/'
    filename = url.split('/')[-1]
    download_zip(url, path, filename)

    path = 'test_output/'
    filename = 'gl1871.zip'
    loc = 'test_output/test_unzip'
    unzip_file(path, filename, loc)

    'test-change''