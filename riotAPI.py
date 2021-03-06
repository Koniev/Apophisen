# -*- coding: utf-8 -*-

"""
Do not forget to pip install RiotWatcher before anything
"""
import datetime
import time
import sys
from riotwatcher import RiotWatcher, ApiError
"""
Put your API key here, it is mine (Koniev)
"""

tierList = ['DIAMOND', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON']
divisionList = ['I', 'II', 'III', 'IV']
watcher = RiotWatcher('RGAPI-66ac386a-572c-44bc-8185-029275086fec')

my_region = 'euw1'
my_queue = 'RANKED_SOLO_5x5'

"""
if we want to go through the whole thing

for t in tier:
    for d in division:
        for i in range(1, 10):
            getTotalKills(my_region, my_queue, t, d, i)
"""
"""
Function used to get summonerId based on standard infos
"""
def getSummonerId(region, queue, tier, division, page):
    try:
        userData = watcher.league.entries(region, queue, tier, division, page)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
            time.sleep(120)
            getSummonerId(region, queue, tier, division, page)
        else:
            raise
    sumId = []
    for item in userData:
        sumId.append(item.get('summonerId'))
    return sumId

"""
Morph the userId into accountId
"""
def getAccountId(userId):
    try:
        accId = watcher.summoner.by_id(my_region, userId)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
            time.sleep(120)
            getAccountId(userId)
        else:
            raise
    return accId
"""
Return gamesId depending of the accountId of the player
"""
def getGamesId(accId):
    try:
        matches = watcher.match.matchlist_by_account(my_region, accId.get('accountId'))
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
            time.sleep(120)
            getGamesId(accId)
        else:
            raise
    return [i.get('gameId') for i in matches.get('matches')]

"""
Return the total number of kills and the gameCreation date for a game
"""
def getTotalKillsAndCreation(gameId):
    try:
        infos = watcher.match.by_id(my_region, gameId)
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
            time.sleep(120)
            getTotalKillsAndCreation(gameId)
        else:
            raise
    """
    Since we now have the match history, it is possible to get the number of kills/game
    """    
    gameCreation = datetime.datetime.fromtimestamp(infos.get('gameCreation')/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
    participantInfos = [i.get('stats') for i in infos.get('participants')]
    participantKills = [item.get('kills') for item in participantInfos]
    """
    The total kill is the sum of every kill of every participant of the game
    """
    totalKills = sum(participantKills)
    return totalKills, gameCreation


#%% Main
for t in tierList:
    print(t)
    for d in divisionList:
        print(d)
        for p in range(1,10):
            print(p)
            sumId = getSummonerId(my_region, my_queue, t, d, p)
            for sId in sumId:
                print(sId)
                accId = getAccountId(sId)
                gamesId = getGamesId(accId)
                for gId in gamesId:
                    total = getTotalKillsAndCreation(gId)
                    with open(sys.path[0] + "\\dataAPIriot.txt", "a") as myfile:
                        myfile.write(str(total[0]) + "," + total[1] + "\n")

