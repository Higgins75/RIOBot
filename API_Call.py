import discord
from discord.ext import commands
import requests

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='.',intents=intents)

response = requests.get('https://raider.io/api/v1/characters/profile?region=eu&realm=draenor&name=gigdh')
#print(response.json())

def GetRioLink():
    return "https://raider.io/characters/"