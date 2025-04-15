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