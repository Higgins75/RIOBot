#Python Lib imports
import os
from typing import Literal

#discord.py import
import discord
from discord.ext import commands

#local files
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("token")

import helpers.SQLite_Funcs as db 
import helpers.API_Funcs as api

#list of Regions for later use
regions = Literal["eu", "na", "kr","tw", "cn"]

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
        
@bot.event
async def on_error(ctx, error):
    await ctx.send("Error found, please try again later")
    

'''#Test command for purging channels
@bot.tree.command(name='purge')
async def purge(interaction: discord.Interaction, amount: int = 100):
    await interaction.response.defer()
    await interaction.channel.purge(limit =  amount)
    await interaction.channel.send(f'channel purged')
'''

#Adds a user profile to the database
@bot.tree.command(name="add_profile")
async def add_profile(interaction: discord.Interaction, region : Literal[regions], realm: str, charactername: str):
    user = str(interaction.user)
    db.insertProfile(user, charactername, region, realm)
    RaiderLinkURL = api.GetRioLink(region, realm, charactername)
    await interaction.user.send(f"Linked your DiscordID to the profile for {RaiderLinkURL}")
    await interaction.response.send_message(f"User Profile added")
    

#Deletes user data from the database
@bot.tree.command(name="delete_profile")
async def delete_profile(interaction: discord.Interaction):
    user = str(interaction.user)
    return_string = db.removeProfile(user)
    await interaction.response.send_message(f'{return_string}')

#checks a user has a profile in the SQLite Database, returns associated character name 
@bot.tree.command(name="check_profile")
async def check_profile(interaction: discord.Interaction):
    user = str(interaction.user)   
    if db.checkUserExists(user) == True:
        userdata = db.getUserData(user)
        _, charactername, _, _ = userdata
        await interaction.response.send_message(f'Profile found for {charactername}')
    else:
        await interaction.response.send_message("Profile not found")

#Generates user's Raider.IO Link from Database Characer
@bot.tree.command(name='rio_link')
async def rio_link(interaction: discord.Interaction):
    user = str(interaction.user)
    if db.checkUserExists == False:
        await interaction.response.send_message("Profile not found. Please add profile to use this command")
    else: 
        userdata = db.getUserData(user)
        if userdata != None:
            _, charactername, region, realm = userdata
            RaiderLinkURL = api.GetRioLink(region, realm, charactername)
            await interaction.response.send_message(f'Your RIO link is {RaiderLinkURL}')

#Generates the user's Raider.IO Score from Database Character
@bot.tree.command(name='rio_score')
async def rio_score(interaction: discord.Interaction):
    user = str(interaction.user)
    
    if not db.checkUserExists(user):
        await interaction.response.send_message("Profile not found. Please add profile to use this command")
        return
    
    userdata = db.getUserData(user)
    if not userdata or len(userdata) < 4:
        await interaction.response.send_message("Error: User profile data is incomplete or missing.")
    
    _, charactername, region, realm = userdata
    Rio_Total = api.GetRIO(region, realm, charactername)
        
    if isinstance(Rio_Total, int):
        await interaction.response.send_message(f'The Raider.IO Score of {charactername} is {Rio_Total}')
    else:
        await interaction.response.send_message(f'An Error occured of type {Rio_Total}')
            
#Generates the user's lowest M+ Keys this season from Database Character 
@bot.tree.command(name='lowest_keys')
async def lowest_keys(interaction: discord.Interaction):
    user = str(interaction.user)
    if db.checkUserExists == False:
        await interaction.response.send_message("Profile not found. Please add profile to use this command")
    else: 
        userdata = db.getUserData(user)
        if userdata != None:
            _, charactername, region, realm = userdata   
            string_return = (api.GetLowestKey(region, realm, charactername))
            await interaction.response.send_message(f'The lowest keys of **{charactername}** are: \n {string_return}')     
            
#to be developed.
@bot.tree.command(name='resilient_keys')
async def resilient_keys(interaction: discord.Interaction):
    await interaction.response.send_message("In development")    

#runs the bot        
bot.run(bot_token)