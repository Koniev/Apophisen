# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 21:15:16 2019

@author: gauti
"""

from riotwatcher import LolWatcher, ApiError
import json
        

watcher = LolWatcher('RGAPI-66ac386a-572c-44bc-8185-029275086fec')
my_region = 'euw1'
my_name = 'Koniev'
my_queue = 420 # 'RANKED_SOLO_5x5'

        
def getPlayerData(region, summonerName, queueNumber):
    try:
        # Get summoner Id
        player = watcher.summoner.by_name(region, summonerName)
        # Then get history based on this Id
        history = watcher.match.matchlist_by_account(region, player.get('accountId'), queueNumber)
        # TO DO : matchDetails to deal with correctly
        # matchsDetails = [watcher.match.by_id(region, match.get('gameId')) for match in history.get('matches')]
        versions = watcher.data_dragon.versions_for_region(region)
        champions_version = versions['n']['champion']
        champInfos = watcher.data_dragon.champions(champions_version)
        champs = {}
        for c in champInfos.get('data'):
            key = champInfos.get('data').get(c).get('key')
            if key not in champs.keys():
                champs[key] = champInfos.get('data').get(c).get('name')
        # Store data in data-SummonerName.json
        with open("data-" + summonerName + ".json","w") as f:
            matches = history.get('matches')            
            for item in matches:
                game = watcher.match.by_id(region, str(item['gameId']))
                item['gameDuration'] = game['gameDuration']
                item['champion']=champs.get(str(item['champion'])) if champs.get(str(item['champion'])) != None else item['champion']
            f.write(json.dumps(matches))
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise
            
getPlayerData(my_region, 'Koniev', my_queue)