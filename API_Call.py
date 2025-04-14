import json
import requests


response = requests.get('https://raider.io/api/v1/characters/profile?region=eu&realm=draenor&name=gigdh')
#print(response.json())

def GetRioLink(region : str, realm: str, charactername: str):
    RaiderLinkURL = "https://raider.io/characters/" + region + '/' + realm + '/' + charactername
    return RaiderLinkURL