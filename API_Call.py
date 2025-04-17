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

#Returns the value of your lowest M+ Run
def GetLowestKey(region : str, realm: str, charactername: str):
    RunsURL = 'https://raider.io/api/v1/characters/profile?region=' + region + '&realm=' + realm + '&name=' + charactername + '&fields=mythic_plus_best_runs'
    runs = requests.get(RunsURL).json()
    
    #init and populate dictionary from API
    dungeon_dict = {}    
    for x in runs['mythic_plus_best_runs']:
        dungeon_dict[x['dungeon']] = x['mythic_level']

    #find lowest M+ Run Value (even if multiple)
    lowest_key = min(dungeon_dict.values())
    
    #Create a new dict of only runs at the lowest M+ level
    lowest_dungeons_dict = {}    
    for key, values in dungeon_dict.items():
        if values == lowest_key:
            lowest_dungeons_dict.update({key: values})
           
    #Creates a concat string of these keys to return
    string_values = []
    for k, v in lowest_dungeons_dict.items():
        string_values.append(f"{k}:  {v}")
    Lowest_key_return = "\n ".join(string_values)

    return Lowest_key_return