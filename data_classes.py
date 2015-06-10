class NoWinnerError(Exception):

    def __init__(self, msg, cond, match):
        self.cond = cond
        self.match = match
        self.msg = msg


class Team(object):

    def __init__(self, db=None, json=None):
        if db is None and json is None:
            raise Exception('Must include at least one non-default to '
                            'instantiate a Team.')
        if db is not None:
            return self.team_from_db(self, db)
        if json is not None:
            return self.team_from_db(self, json)

    def team_from_db(self, db):
        " construct a team object from a database return "
        self.db_key = db[0]
        self.track_id = db[1]
        self.team_id = db[2]
        self.team_tag = db[3]
        self.team_name = db[4]
        self.played_at = db[5]
        self.match_id = db[6]
        self.created_at = db[7]
        self.init_wins = db[8]
        self.init_losses = db[9]
        self.init_tier = db[10]
        self.init_div = db[11]
        self.dead = db[12]
        return self

    def team_from_json(self, json):
        """
        construct a team object from a json.
        User will need to set a number of values in order to have a
        fully-fledged team object for writing to db:
        team_id (which should be known since you just requested the team by id),
        track_id (-1 for a tracked team, other team id if an opponent of a
            tracked team.

        played_at,
        match_id need to be set and should be easy to set if this is
            an opponent, because you have that info when searching for this
            team.

        init_tier, init_div should be set as well by looking the team's rank
            up.
        """
        self.db_key = None  # assigned once put in DB
        self.track_id = None
        self.team_id = None
        self.team_tag = json['tag']
        self.team_name = json['name']
        self.played_at = None
        self.match_id = None
        self.created_at = json['createDate']
        self.init_wins = json['teamStatDetails']['wins']
        self.init_losses = json['teamStatDetails']['losses']
        self.init_tier = None  # Will need to determine through more calls
        self.init_div = None  # Will need to determine through more calls
        self.dead = False
        return self


class Match(object):

    def __init__(self, json):
        self.match_creation = json['matchCreation']
        self.participant_ids = json['participantIdentities']
        self.participants = json['participants']
        self.teams = json['teams']

    def get_players_by_outcome(self, winner):
        """
        Get a list of summoner (id, name) tuples for the team that won or lost
        if winner=True or winner=False, respectively.
        """
        team = None
        for inspect_team in self.teams:
            if winner is inspect_team['winner']:
                team = inspect_team
        if team is None:
            raise NoWinnerError('Match lacks the outcome sought', winner, self)
        pids = []
        for pa in self.participants:
            if pa['teamId'] is team:
                pids.append(pa['participantId'])
        players = []
        for pl in self.participant_ids:
            if pl['participantId'] in pids:
                players.append((pl['Player']['summonerId'],
                                pl['player']['summonerName']))
        return players


class League(object):
    pass
