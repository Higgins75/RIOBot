import json
import requests


#Gets a user's raider.io link
def GetRioLink(region : str, realm: str, charactername: str):
    RaiderLinkURL = "https://raider.io/characters/" + region + '/' + realm + '/' + charactername
    return RaiderLinkURL

#calls Raider.IO Api and returns the score information from the JSON
def GetRIO(region : str, realm: str, charactername: str):
    RequestURL = 'https://raider.io/api/v1/characters/profile?region=' + region + '&realm=' + realm + '&name=' + charactername + '&fields=mythic_plus_scores_by_season%3Aseason-tww-2'
    info = requests.get(RequestURL).json()
    info_keys = (info["mythic_plus_scores_by_season"][0])
    scores = info_keys["scores"]
    return (scores['all'])

#In development
def GetBestRuns(region : str, realm: str, charactername: str):
    RunsURL = 'https://raider.io/api/v1/characters/profile?region=' + region + '&realm=' + realm + '&name=' + charactername + '&fields=mythic_plus_best_runs'
    runs = requests.get(RunsURL).json()
    
    dungeon_names = []
    dungeon_tiers = []

    for x in runs['mythic_plus_best_runs']:
        dungeon_names.append(x['dungeon'])
        dungeon_tiers.append(x['mythic_level'])

    
    lowest_key = (min((dungeon_tiers)))          
  
    return lowest_key 