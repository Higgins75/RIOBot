import json
import requests


def GetRioLink(region : str, realm: str, charactername: str):
    RaiderLinkURL = "https://raider.io/characters/" + region + '/' + realm + '/' + charactername
    return RaiderLinkURL

def GetRIO(region : str, realm: str, charactername: str):
    RequestURL = 'https://raider.io/api/v1/characters/profile?region=' + region + '&realm=' + realm + '&name=' + charactername + '&fields=mythic_plus_scores_by_season%3Aseason-tww-2'
    info = requests.get(RequestURL).json()
    info_keys = (info["mythic_plus_scores_by_season"][0])
    scores = info_keys["scores"]
    return (scores['all'])


def GetBestRuns(region : str, realm: str, charactername: str):
    RunsURL = 'https://raider.io/api/v1/characters/profile?region=' + region + '&realm=' + realm + '&name=' + charactername + '&fields=mythic_plus_best_runs'
    runs = requests.get(RunsURL).json()
    dungeon_dict = {}
    for x in runs['mythic_plus_best_runs']:
        #print (runs['mythic_plus_best_runs'])
        #print(f' {x['dungeon']} is at {x['mythic_level']}')
        dungeon_name = str(x['dungeon'])
        dungeon_level = int(x['mythic_level'])
        dungeon_dict.update({dungeon_name : dungeon_level})
    
    lowest_key = min(dungeon_dict)
    #print(f'The lowest key of {charactername} is {lowest_key}')
    #print (dungeon_dict)
    return lowest_key