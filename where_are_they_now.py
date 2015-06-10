#!/usr/bin/python
import sys
import pprint
from process_match import process_match
from make_request import make_request

team_id = sys.argv[1]
api_key = sys.argv[2]
s = 'https://na.api.pvp.net/api/lol/na/v2.4/team/' \
    '{0}?api_key={1}'.format(team_id, api_key)
try:
    r = make_request(s)
except Exception as e:
    print('Attempt to get team history failed.')
    print(e)
    quit()
j = r.json()
th = j[team_id]
mh = th['matchHistory']
print('{} Matches:'.format(len(mh)))
summary = []
for m in mh:
    # print(json.dumps(m, sort_keys=True, indent=2))
    print('{5} Against {0}, win = {1}, kda {2}/{3}/{4}'.format(
        m['opposingTeamName'], m['win'], m['kills'], m['deaths'], m['assists'],
        m['gameId']))
    ms = process_match(m, api_key)
    if ms is None:
        ms = dict(lookup_fail='All players left team')
    if m['win']:
        ms['outcome'] = 'win'
    else:
        ms['outcome'] = 'lose'
    ms['opponent'] = m['opposingTeamName']
    summary.append(ms)

print('All Done!')
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(summary)
