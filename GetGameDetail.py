# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:21:55 2019

@author: gauti
"""


from riotwatcher import RiotWatcher, ApiError
import json
        

watcher = RiotWatcher('RGAPI-e64d043b-400e-42a2-8a3a-07e387e18ac9')
my_region = 'euw1'


def getGameData(region, gameId):
    try:
        # Get game details
        game = watcher.match.by_id(region, gameId)
        # TO DO : matchDetails to deal with correctly
        # matchsDetails = [watcher.match.by_id(region, match.get('gameId')) for match in history.get('matches')]
        with open('9.19.1/data/fr_FR/champion.json', "r") as champData:
            champJson = json.load(champData)
        champInfos = champJson.get('data')
        champs = {}
        for c in champInfos:
            key = champInfos.get(c).get('key')
            if key not in champs.keys():
                champs[key] = champInfos.get(c).get('name')
        # Store data in data-SummonerName.json
        with open("gameData-" + gameId + ".json","w") as f:
            for item in game['participants']:
                item['championId'] = champs.get(str(item['championId'])) if champs.get(str(item['championId'])) != None else item['championId']
            f.write(json.dumps(game))
    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')
        else:
            raise
            
getGameData(my_region, '4211509827')