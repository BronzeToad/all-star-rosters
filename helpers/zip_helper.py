import requests


def download_zip(url, path, filename):
    zip = requests.get(url)
    with open(f'{path}{filename}', 'wb') as f:
        f.write(zip.content)


if __name__ == '__main__':
    print('Executing as standalone script')

    url = 'https://www.retrosheet.org/gamelogs/gl1871.zip'
    path = 'test_output/'
    filename = url.split('/')[-1]

    download_zip(url, path, filename)