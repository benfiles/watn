import query_library as ql
from data_classes import (Team, Match, League)

# These guys just over-write attributes of the QueryLibrary superclass.
# Initialize by giving the argument and the api_key


class MatchById(ql.QueryLibrary):
    query_str = ql.match_by_id  # test
    return_class = Match


class TeamListGetter(ql.QueryLibrary):

    " Superclass for classes that need to return a list of teams "

    def get(self):
        r = self.make_request(self.query)
        big_json = r.json()
        team_list = ()
        for team_id in big_json:
            team = Team(json=big_json[team_id])
            team.team_id = team_id
            team_list.append(team)
        return team_list


class TeamBySummonerId(TeamListGetter):
    query_str = ql.summoner_by_id
    return_class = Team


class TeamByTeamId(TeamListGetter):
    query_str = ql.team_by_team_id
    return_class = Team


class LeagueByTeamId(ql.QueryLibrary):
    query_str = ql.league_by_team_id
    return_class = League
