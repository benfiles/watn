import query_library.QueryLibrary

# These guys just over-write attributes of the QueryLibrary superclass.
# Initialize by giving the argument and the api_key

class MatchById(QueryLibrary):
    query_str = match_by_id
    return_class = Match

class TeamBySummonerId(QueryLibrary):
    query_str = summoner_by_id
    return_class = Team

class LeagueByTeamId(QueryLibrary):
    query_str = league_by_team_id
    return_class = League

class TeamByTeamId(QueryLibrary):
    query_str = team_by_team_id
    return_class = Team
