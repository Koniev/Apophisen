# -*- coding: utf-8 -*-

"""
Do not forget to pip install RiotWatcher before anything
"""
import datetime
import sys
from riotwatcher import RiotWatcher, ApiError
"""
Put your API key here, it is mine (Koniev)
"""

tierList = ['DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
divisionList = ['I', 'II', 'III', 'IV']
watcher = RiotWatcher('RGAPI-be037780-90a0-4fa5-b182-69976e7e7b1f')

my_region = 'euw1'
my_queue = 'RANKED_SOLO_5x5'

"""
if we want to go through the whole thing

for t in tier:
    for d in division:
        for i in range(1, 10):
            getTotalKills(my_region, my_queue, t, d, i)
"""
def getTotalKills(region, queue, tier, division, page):
    try:
        watcher.league.entries(region, queue, tier, division, page)
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
    Since we know have summoner info, we want entries for the dict, then we will use it to get the sumId
    """
    data = challengers.get('entries')
    sumId = []
    for item in data:
        sumId.append(item.get('summonerId'))
    """
    Here it is an example, but we need to ask the accountId for every summonerId to get the machId using the accountId
    """
    accId = watcher.summoner.by_id(my_region, sumId[0])
    matches = watcher.match.matchlist_by_account(my_region, accId.get('accountId'))
    gameId = [i.get('gameId') for i in matches.get('matches')]
    """
    Since we now have the match history, it is possible to get the number of kills/game
    """
    infos = watcher.match.by_id(my_region, gameId[0])
    gameCreation = datetime.datetime.fromtimestamp(infos.get('gameCreation')/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    participantInfos = [i.get('stats') for i in infos.get('participants')]
    participantKills = [item.get('kills') for item in participantInfos]
    """
    The total kill is the sum of every kill of every participant of the game
    """
    totalKills = sum(participantKills)
    return totalKills, gameCreation

print(getTotalKills(my_region, my_queue, tierList[0], divisionList[0], 1))
