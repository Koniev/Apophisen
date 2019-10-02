# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 21:15:16 2019

@author: gauti
"""

from riotwatcher import RiotWatcher, ApiError
import json
        

watcher = RiotWatcher('RGAPI-2a5a45a4-f1fd-43e7-aa3b-c7983c9c643a')
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
        with open('9.19.1/data/fr_FR/champion.json', "r") as champData:
            champJson = json.load(champData)
        champInfos = champJson.get('data')
        champs = {}
        for c in champInfos:
            key = champInfos.get(c).get('key')
            if key not in champs.keys():
                champs[key] = champInfos.get(c).get('name')
        # TO DELETE : dump champion references just to check if it is working correctly
        with open("champRef.json", "w") as r:
             r.write(json.dumps(champs))
        # Store data in data-SummonerName.json
        with open("data-" + summonerName + ".json","w") as f:
            matches = history.get('matches')
            for item in matches:
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
#getPlayerData(my_region, 'Neekoptère', my_queue)
#getPlayerData(my_region, 'PieraptorR', my_queue)