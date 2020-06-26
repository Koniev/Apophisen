# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 22:21:55 2019

@author: gauti
"""


from riotwatcher import LolWatcher, ApiError
import json
        

watcher = LolWatcher('RGAPI-66ac386a-572c-44bc-8185-029275086fec')
my_region = 'euw1'
my_queue = 420 # 'RANKED_SOLO_5x5'

class Player:
    Champion = ""
    Kills = 0
    Deaths = 0
    Assists = 0
    Damages = 0
    VisionScore = 0
    VisionWards = 0
    WardsKilled = 0
    WardsPlaced = 0
    GoldEarned = 0
    def __init__(self, 
                 name, 
                 team,
                 champion=None, 
                 kills=None, 
                 deaths=None, 
                 assists=None, 
                 damages=None,
                 visionScore=None,
                 visionWards=None,
                 wardsKilled=None,
                 wardsPlaced=None,
                 goldEarned=None):
        self.name = name
        self.Team = team
        self.Champion = champion
        self.Kills = kills
        self.Deaths = deaths
        self.Assists = assists
        self.Damages = damages
        self.VisionScore = visionScore
        self.VisionWards = visionWards
        self.WardsKilled = wardsKilled
        self.WardsPlaced = wardsPlaced
        self.GoldEarned = goldEarned
    def __str__(self):
        string = ""
        for name, value in vars(self).items():
            string += name + ": " + str(value) + "\n"
        return string
    
def GetPlayerMatches(region, queueNumber, playerName):
    # Get summoner Id
    player = watcher.summoner.by_name(region, playerName)
    # Then get history based on this Id
    history = watcher.match.matchlist_by_account(region, player.get('accountId'), queueNumber)
    return history.get('matches')
    
def getGameData(region, gameId):
    try:
        # Get game details
        game = watcher.match.by_id(region, gameId)
        # TO DO : matchDetails to deal with correctly
        # matchsDetails = [watcher.match.by_id(region, match.get('gameId')) for match in history.get('matches')]
        listOfPlayers = []
        versions = watcher.data_dragon.versions_for_region(region)
        champions_version = versions['n']['champion']
        champInfos = watcher.data_dragon.champions(champions_version)
        champs = {}
        for c in champInfos.get('data'):
            key = champInfos.get('data').get(c).get('key')
            if key not in champs.keys():
                champs[key] = champInfos.get('data').get(c).get('name')
        # Store data in data-GameID.json
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
                listOfPlayers.append(Player(item['participantId'], 
                                            item['teamId'],
                                            item['championId'],
                                            stats['kills'], 
                                            stats['deaths'], 
                                            stats['assists'], 
                                            stats['totalDamageDealtToChampions'],
                                            stats['visionScore'],
                                            stats['visionWardsBoughtInGame'],
                                            stats['wardsKilled'],
                                            stats['wardsPlaced'],
                                            stats['goldEarned']
                                            ))
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
#%%        

matches = GetPlayerMatches(my_region, my_queue, "Koniev")
for match in matches:
    getGameData(my_region, str(match['gameId']))
