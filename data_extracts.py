from AllStar_MeanGirls.helpers.zip_helper import ZipHelper

url = 'https://github.com/chadwickbureau/baseballdatabank/archive/refs/tags/v2022.2'
folder = 'data/lahmans'

lahmans = ZipHelper(download_url=url, folder=folder, filename='test')
lahmans.get_zip()

https://github.com/chadwickbureau/baseballdatabank/blob/79f84472bb8ac7ce7b79e143a2accdcdc91a7147/core/AllstarFull.csv