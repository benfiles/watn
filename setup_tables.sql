/* Table teams
    This table contains a list of teams.  It stores information about teams to
    track as well as their opponents. Whenever a tracked team is found
    to have played a team that does not exist in this table as an opponent of
    theirs, then that team gets added to this table. The idea is that we will
    periodically check in on these teams to see how they are doing now.

    I'm including information about their initial situation; ideally we would
    get this right after the first game, but we'll just accept that the 
    'initial' designation is approximate.

    The track_id column is kind of weird.  If the value is -1, it implies that 
    the team described by that row is a 'tracked team'.  Otherwise, track_id is
    the rowid of a tracked team.  In that case, the team described on the 
    row in question was an opponent of that tracked team.

    So, to get all the opponents we know of about the team on row 1, we would:
    SELECT * from teams WHERE track_id = 1;
    (or the correct SQL syntax for that approximate idea).
*/
CREATE TABLE teams (
    team        INTEGER PRIMARY KEY,
    track_id    INTEGER,  -- which tracked team did they play?
                          -- -1 in this field indicates a tracked team.
    team_id     TEXT,     -- Riot's id for this team
    team_tag    TEXT,     -- opponents team tag
    team_name   TEXT,     -- Human readable team name
    played_at   INTEGER,  -- Time of game vs tracked team, null for tracked
    match_id    INTEGER,  -- Riot's ID number for the match, null for tracked
    created_at  INTEGER,  -- Time the team was created
    init_wins   INTEGER,  -- Number of wins at first check
    init_losses INTEGER,  -- Number of losses at first check
    init_tier   INTEGER,  -- Tier at first check
    init_div    INTEGER,  -- Division at first check
    dead        INTEGER  -- Flag for if we want to stop tracking them.
    );

/* Table Observations
    Here is where we store periodic observations of teams and opponents.

    I'll timestamp each observation, so that the most recent observation can be
    pulled up easily. If a team has had no activity since the last observation
    then we don't need to add a row to the databse, instead we can just update
    the timestamp.
*/
CREATE TABLE observations (
    obs         INTEGER PRIMARY KEY,
    obs_team    INTEGER,    -- rowid in teams db
    obs_time    INTEGER,    -- as of when is this obs current?
    wins        INTEGER,    -- total wins observed
    losses      INTEGER,    -- total losses observed
    tier        INTEGER,    -- observed tier
    div         INTEGER,    -- observed division
    recent_game INTEGER,    -- time of the most recent game
    FOREIGN KEY(obs_team) REFERENCES teams(team)
    );

