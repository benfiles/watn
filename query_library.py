import requests
import time
class QueryLibrary:
    """ Contains query constants and functions for making LOL API calls """
    region = 'na'
    base_url = 'https://'+region+'.api.pvp.net/api/lol/'+region+'/'

    # Version numbers
    v_match_by_id = 'v2.2'
    v_team_by_summoner_id = 'v2.4'
    v_league_by_team_id = 'v2.5'
    v_match_by_match_id = 'v2.2'
    v_team_by_team_id = 'v2.4'

    # Queries Ready for Format
    match_by_id = base_url+v_match_by_id+'/match/{0}?api_key={1}'
    team_by_summoner_id = base_url+v_team_by_summoner_id+'/team/by-summoner/' \
                          '{0}?api_key={1}'
    league_by_team_id = base_url+v_league_by_team_id+'/league/by-team/{0}/' \
                        'entry?api_key={1}'
    match_by_match_id = base_url+v_match_by_match_id+'/match/{0}?api_key={1}'
    team_by_team_id = base_url+v_team_by_team_id+'/team/{0}?api_key={1}'
    # Unofficial abstract properties
    query_str = ''
    return_class = ''
    def __init__(self,arg,key):
        self.query = query_str.format(match_id,api_key)
    def get(self):
        r = make_request(self.query)
        return return_class(json=r.json())
    def make_request(str):
        """
        Makes a requests.get call.  If return code is 429, pause for 10
        seconds and try again. If return code is not 200 after that, raises a
        generic exception.
        """
        r = requests.get(str)
        if r.status_code == 429:
            print('-- Rate Limit Exceeded. Pausing for 10 seconds...')
            time.sleep(10)
            r = make_request(str)
        if r.status_code != 200:
            raise Exception('Return status code {}'.format(r.status_code))
        return r
