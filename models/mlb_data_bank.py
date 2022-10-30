import helpers.data_helpers as DataHelper


class BaseballDataBank:
    BASE_URL = 'https://raw.githubusercontent.com/chadwickbureau/baseballdatabank/master/'
    
    CONTRIB = [
        'AwardsManagers',
        'AwardsPlayers',
        'AwardsShareManagers',
        'AwardsSharePlayers',
        'CollegePlaying',
        'HallOfFame',
        'Salaries',
        'Schools'
    ]
        
    CORE = [
        'AllstarFull', 
        'Appearances', 
        'Batting', 
        'BattingPost', 
        'Fielding', 
        'FieldingOF',
        'FieldingOFsplit',
        'FieldingPost',
        'HomeGames',
        'Managers',
        'ManagersHalf',
        'Parks',
        'People',
        'Pitchiing',
        'PitchingPost',
        'SeriesPost'
        'Teams'
        'TeamsFranchises'
        'TeamsHalf'
    ]
    
    UPSTREAM = [
        'Teams'
    ]
    
    
    def __init__(self, url_list: list = []):
        self.url_list = url_list
    
    
    def get_urls(self, 
                 base_url: str = BASE_URL, 
                 contrib: str = CONTRIB, 
                 core: str = CORE, 
                 upstream: str = UPSTREAM):
        
        for file in contrib:
            self.url_list.append(f'{base_url}/contrib/{file}.csv')
            
        for file in core:
            self.url_list.append(f'{base_url}/core/{file}.csv')
            
        for file in upstream:
            self.url_list.append(f'{base_url}/upstream/{file}.csv')
    
    
    def get_data(self):
        if len(self.url_list) == 0:
            self.get_urls()
        for url in self.url_list:
            DataHelper.download_from_url(url=url, folder='data/baseball_databank')
    
    
if __name__ == '__main__':
    print('Executing as standalone script')
    
    databank = BaseballDataBank()
    databank.get_data()