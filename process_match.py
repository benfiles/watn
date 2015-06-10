from query_library import (MatchById, TeamBySummonerId)


def process_match(mh, api_key):
    """
    Given a match structure from a team's match history, hunt down the current
    league tier and division. Prints a bunch, and returns a dict with some
    output summary
    """
    match_id = mh['gameId']
    opponent_victory = not mh['win']  # if we won, the opponent is whoever lost
    mbi = MatchById(match_id, api_key)
    m = mbi.get()
    opponent_players = m.get_players_by_outcome(opponent_victory)
    # ok, we have a summoner id for someone on the oppsing team.
    # now we get all the teams that summoner is on to find the team
    # we played against.
    opponent = None
    for opp in opponent_players:
        opp_summoner_id = opp(0)
        tbsi = TeamBySummonerId(opp_summoner_id, api_key)
        teams = tbsi.get()
        for team in teams:
            if team.team_name is mh['opposingTeam']:
                opponent = team # found the opponent!
                break
        if opponent is not None:
            break
    if opponent is None:
        # opponent team no longer exists!
        # I'll need to handle this somehow, but for now I leave things here.
        pass
    # Next Steps:
    # Write opponent to database table
    #
#                team_by_summoner_fmt = 'https://na.api.pvp.net/api' \
#                                       '/lol/na/v2.4/team/by-summoner/' \
#                                       '{}?api_key={}'
#                team_by_summoner_qry = team_by_summoner_fmt.format(
#                    opp_summoner_id, api_key)
#                print('Getting teams by summoner...')
#                try:
#                    teamlist_req = make_request(team_by_summoner_qry)
#                except Exception as e:
#                    print('Problem getting teamlist by summoner ID')
#                    print(e)
#                    continue
#                print(teamlist_req.status_code)
#                teamlist_json = teamlist_req.json()
#                for team_candidate in teamlist_json[str(opp_summoner_id)]:
#                    if team_candidate['name'] == m['opposingTeamName']:
#                        opp_id = team_candidate['fullId']
# okay, we have the team! Find out where it stands.
# Print their current record
#                        print('team {} record:'.format(team_candidate['name']))
#                        for detail in team_candidate['teamStatDetails']:
#                            if detail['teamStatType']=='RANKED_TEAM_5x5':
#                                print('W:{} L:{} {}'.format(
#                                      detail['wins'],detail['losses'],
#                                      detail['teamStatType']))
#                                break
# Get their current league info
#                        opp_fmt = 'https://na.api.pvp.net/api/lol/na/' \
#                            'v2.5/league/by-team/{}/entry?api_key={}'
#                        opp_qry = opp_fmt.format(opp_id,api_key)
#                        print('Looking up opponent league...')
#                        try:
#                            opp_req = make_request(opp_qry)
#                        except Exception as e:
#                            print('Could not find opponent league')
#                            print(e)
#                            return {'Wins': detail['wins'],
#                                    'Losses': detail['losses'],
#                                    'Rank': 'none'
#                                   }
#                        opp_json = opp_req.json()
# teams can have different leagues per queue
#                        for opp_league_dict in opp_json[opp_id]:
#                            if opp_league_dict['queue'] == 'RANKED_TEAM_5x5':
#                                opp_dict = opp_league_dict
#                        for entry in opp_dict['entries']:
#                            if entry['playerOrTeamId'] == opp_id:
#                                print('opponent is currently {} {}.'.format(
#                                   opp_dict['tier'],entry['division']))
#                                dt_ms = team_candidate['lastGameDate'] - \
#                                   m['date']
#                                td = timedelta(milliseconds=dt_ms)
#                                print('Time between our game and their most ' \
#                                      'recent:')
#                                print(td)
#                                return {'Wins': detail['wins'],
#                                        'Losses': detail['losses'],
#                                        'Rank': opp_dict['tier']+' '+
#                                                entry['division'],
#                                        'LivedAtLeast': td.days
#                                       }
