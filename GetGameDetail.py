# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:21:55 2019

@author: gauti
"""


from riotwatcher import RiotWatcher, ApiError
import json
        

watcher = RiotWatcher('RGAPI-22522138-52b3-419f-84ac-bc8e1146c813')
my_region = 'euw1'


class Player:
    Lane = ""
    Champion = ""
    Kills = 0
    Deaths = 0
    Assists = 0
    Damages = 0
    def __init__(self, name, team, champion=None, lane=None,  kills=None, deaths=None, assists=None, damages=None):
        self.name = name
        self.Team = team
        self.Lane = lane
        self.Champion = champion
        self.Kills = kills
        self.Deaths = deaths
        self.Assists = assists
        self.Damages = damages
    def __str__(self):
        string = ""
        for name, value in vars(self).items():
            string += name + ": " + str(value) + "\n"
        return string
def getGameData(region, gameId):
    try:
        # Get game details
        game = watcher.match.by_id(region, gameId)
        # TO DO : matchDetails to deal with correctly
        # matchsDetails = [watcher.match.by_id(region, match.get('gameId')) for match in history.get('matches')]
        listOfPlayers = []
        with open('9.19.1/data/fr_FR/champion.json', "r") as champData:
            champJson = json.load(champData)
        champInfos = champJson.get('data')
        champs = {}
        for c in champInfos:
            key = champInfos.get(c).get('key')
            if key not in champs.keys():
                champs[key] = champInfos.get(c).get('name')
        # Store data in data-SummonerName.json
        playerDict = {}
        for player in game['participantIdentities']:
            key = player['participantId']
            if key not in playerDict.keys():
                playerDict[key] = player['player'].get('summonerName')
        with open("gameData-" + gameId + ".json","w") as f:
            for item in game['participants']:
                item['championId'] = champs.get(str(item['championId'])) if champs.get(str(item['championId'])) != None else item['championId']
                item['participantId'] = playerDict.get(item['participantId'])
                stats = item['stats']
                listOfPlayers.append(Player(item['participantId'], item['teamId'],item['championId'],"BOTTOM", stats['kills'], stats['deaths'], stats['assists'], stats['totalDamageDealtToChampions']))               
            f.write(json.dumps([player.__dict__ for player in listOfPlayers]))
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