# -*- coding: utf-8 -*-

"""
Do not forget to pip install RiotWatcher before anything
"""
from riotwatcher import RiotWatcher, ApiError
"""
Put your API key here, it is mine (Koniev)
"""

watcher = RiotWatcher('RGAPI-be037780-90a0-4fa5-b182-69976e7e7b1f')

my_region = 'euw1'
my_queue = 'RANKED_SOLO_5x5'

try:
    """
    get a number of summoner info
    """
    challengers = watcher.league.challenger_by_queue(my_region, my_queue)
except ApiError as err:
    if err.response.status_code == 429:
        print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
        print('this retry-after is handled by default by the RiotWatcher library')
        print('future requests wait until the retry-after time passes')
    elif err.response.status_code == 404:
        print('Summoner with that ridiculous name not found.')
    else:
        raise
"""
Since we now have summoner info, we want entries for the dict, then we will use it to get the sumId
"""
data = challengers.get('entries')
sumId = []
matches = []
for item in data:
    sumId.append(item.get('summonerId'))
"""
Here it is an example, but we need to ask the accountId for every summonerId to get the machId using the accountId
"""
accId = watcher.summoner.by_id(my_region, sumId[0])
matches = watcher.match.matchlist_by_account(my_region, accId.get('accountId'))
print(matches.get('matches')[0])

"""
Since we now have the match history, it is possible to get the number of kills/game
"""
