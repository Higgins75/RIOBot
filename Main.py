import discord
from typing import Literal
from discord.ext import commands
from Bot_Token import token
from SQLite_Funcs import insertProfile
from SQLite_Funcs import checkUserExists
from SQLite_Funcs import removeProfile
from API_Call import GetRioLink
from API_Call import GetRIO
from API_Call import GetLowestKey
from Lists import regions

#Sets up Discord
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='.',intents=intents)

#Readys the Bot, prints messages to CLI to allow for Command Debug
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


#Adds a user profile, currently used as a test case.
@bot.tree.command(name="add_profile")
async def add_profile(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    user = str(interaction.user)
    insertProfile(user, charactername, region, realm)
    await interaction.response.send_message(f"Running SQL")
    
@bot.tree.command(name="delete_profile")
async def delete_profile(interaction: discord.Interaction):
    user = str(interaction.user)
    return_string = removeProfile(user)
    await interaction.response.send_message(f'{return_string}')

#checks a user has a profile in the SQLite Database    
@bot.tree.command(name="check_profile")
async def check_profile(interaction: discord.Interaction):
    user = str(interaction.user)   
    if checkUserExists(user) == True:
        await interaction.response.send_message("Profile found")
    else:
        await interaction.response.send_message("Profile not found")
   
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
    string_return = (GetLowestKey(region, realm, charactername))
    await interaction.response.send_message(f'The lowest keys of **{charactername}** are: \n {string_return}')

#runs the bot        
bot.run(token)