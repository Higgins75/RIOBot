import discord
import sqlite3
import json
import requests
from typing import Literal
from discord.ext import commands
from Bot_Token import token
from API_Call import GetRioLink
from API_Call import GetRIO
from API_Call import GetBestRuns
from Lists import regions

#Sets up Discord
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='.',intents=intents)

#calls the SQL Database associated with this file
con = sqlite3.connect("player_data.db")

#Readys the Bot, prints messages to CLI to allow for Command Debug
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

#General Test Command, currently replies 'Hey @user'
@bot.tree.command(name="tests")
async def test(interaction: discord.Interaction):

    await interaction.response.send_message(f"Hey {interaction.user.mention}!")
    
#Command to reply with a users Raider.IO Link - Requires Error catching    
@bot.tree.command(name="raidlink")
async def raidlink(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    RaiderLinkURL = GetRioLink(region, realm, charactername)
    await interaction.response.send_message(f'Your RIO link is {RaiderLinkURL}')

#Command to return a users Raider.IO Score for the current season    
@bot.tree.command(name='rio')
async def rio(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    Rio_Total = GetRIO(region, realm, charactername)
    await interaction.response.send_message(f'The Raider.IO Score of {charactername} is {Rio_Total}')

#Command in progress of development.    
@bot.tree.command(name='best_runs')
async def runs(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    lowest_key = GetBestRuns(region, realm, charactername)
    await interaction.response.send_message(f'The minimum key of {charactername} is {lowest_key}')

#runs the bot        
bot.run(token)