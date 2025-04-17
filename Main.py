import discord
import sqlite3
import json
import requests
from typing import Literal
from discord.ext import commands
from Bot_Token import token
from API_Call import GetRioLink
from API_Call import GetRIO
from API_Call import GetLowestKey
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

#test functionality for replying to DMs        
@bot.event
async def on_message(message: discord.Message):
    if message.guild is None and not message.author.bot:
        print(message.content)
    await bot.process_commands(message)

#General Test Command, currently replies 'Hey @user'
@bot.tree.command(name="tests")
async def test(interaction: discord.Interaction):
    await interaction.user.send(f"I can DM you now too!")
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")
   
 #Test functionality for DMing the user   
@bot.tree.command(name='dm')
async def DM(interaction: discord.Interaction):
    await interaction.user.send(f'I can DM you now too {interaction.user}')
    await interaction.response.send_message('On it!')
    
    
    
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

#Returns the lowest M+ Runs done this season for a user 
@bot.tree.command(name='lowest_key')
async def runs(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    
    #Gets a dict of lowest M+ runs this season from char
    lowest_key = (GetLowestKey(region, realm, charactername))
    
    #Creates a concat string of these keys to return
    concatstr = ""
    for item in lowest_key:
        concatstr += f'{item} : {lowest_key[item]} \n'

    #Returns to user
    await interaction.response.send_message(f'The Lowest keys of {charactername} are: \n {concatstr}')

#runs the bot        
bot.run(token)