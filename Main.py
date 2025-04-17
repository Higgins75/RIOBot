import discord
from typing import Literal
from discord.ext import commands
from Bot_Token import token
from SQLite_Funcs import insertProfile
from SQLite_Funcs import checkUserExists
from SQLite_Funcs import removeProfile
from SQLite_Funcs import getUserData
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


#Adds a user profile to the database
@bot.tree.command(name="add_profile")
async def add_profile(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    user = str(interaction.user)
    insertProfile(user, charactername, region, realm)
    await interaction.response.send_message(f"Linked your DiscordID to the profile for {charactername}")

#Deletes user data from the database
@bot.tree.command(name="delete_profile")
async def delete_profile(interaction: discord.Interaction):
    user = str(interaction.user)
    return_string = removeProfile(user)
    await interaction.response.send_message(f'{return_string}')

#checks a user has a profile in the SQLite Database, returns associated character name 
@bot.tree.command(name="check_profile")
async def check_profile(interaction: discord.Interaction):
    user = str(interaction.user)   
    if checkUserExists(user) == True:
        userdata = getUserData(user)
        _, charactername, _, _ = userdata
        await interaction.response.send_message(f'Profile found for {charactername}')
    else:
        await interaction.response.send_message("Profile not found")

#Generates user's Raider.IO Link from Database Characer
@bot.tree.command(name='rio_link')
async def rio_link(interaction: discord.Interaction):
    user = str(interaction.user)
    if checkUserExists == False:
        await interaction.response.send_message("Profile not found. Please add profile to use this command")
    else: 
        userdata = getUserData(user)
        if userdata != None:
            _, charactername, region, realm = userdata
            RaiderLinkURL = GetRioLink(region, realm, charactername)
            await interaction.response.send_message(f'Your RIO link is {RaiderLinkURL}')

#Generates the user's Raider.IO Score from Database Character
@bot.tree.command(name='rio_score')
async def rio_score(interaction: discord.Interaction):
    user = str(interaction.user)
    if not checkUserExists(user):
        await interaction.response.send_message("Profile not found. Please add profile to use this command")
        return
    
    userdata = getUserData(user)
    if userdata and len(userdata) >= 4:
        _, charactername, region, realm = userdata
        Rio_Total = GetRIO(region, realm, charactername)
        await interaction.response.send_message(f'The Raider.IO Score of {charactername} is {Rio_Total}')
    else:
        await interaction.response.send_message("User profile data is incomplete or missing.")
            
#Generates the user's lowest M+ Keys this season from Database Character 
@bot.tree.command(name='lowest_keys')
async def lowest_keys(interaction: discord.Interaction):
    user = str(interaction.user)
    if checkUserExists == False:
        await interaction.response.send_message("Profile not found. Please add profile to use this command")
    else: 
        userdata = getUserData(user)
        if userdata != None:
            _, charactername, region, realm = userdata   
            string_return = (GetLowestKey(region, realm, charactername))
            await interaction.response.send_message(f'The lowest keys of **{charactername}** are: \n {string_return}')         

#runs the bot        
bot.run(token)