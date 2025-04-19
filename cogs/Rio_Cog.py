# Python Lib imports
import os
from typing import Literal

# discord.py import
import discord
from discord.ext import commands

import helpers.SQLite_Funcs as db 
import helpers.API_Funcs as api

# List of Regions for later use
regions = Literal["eu", "na", "kr", "tw", "cn"]

class rio_commands(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot

    # Generates user's Raider.IO Link from Database Character
    @discord.app_commands.command(name="rio_link", description="Return any saved Raider.IO Links")
    async def rio_link(self, interaction: discord.Interaction):
        user = str(interaction.user)
        if not db.checkUserExists(user):
            await interaction.response.send_message("Profile not found. Please add profile to use this command")
        else: 
            userdata = db.getUserData(user)
            if userdata is not None:
                _, charactername, region, realm = userdata
                RaiderLinkURL = api.GetRioLink(region, realm, charactername)
                await interaction.response.send_message(f'Your RIO link is {RaiderLinkURL}')

    # Generates the user's Raider.IO Score from Database Character
    @discord.app_commands.command(name="rio_score", description="Return saved profile's Raider.IO Score")
    async def rio_score(self, interaction: discord.Interaction):
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
            await interaction.response.send_message(f'An Error occurred of type {Rio_Total}')
            
    # Generates the user's lowest M+ Keys this season from Database Character
    @discord.app_commands.command(name="lowest_keys", description="Gets the users lowest runs this season")
    async def lowest_keys(self, interaction: discord.Interaction):
        user = str(interaction.user)
        if not db.checkUserExists(user):
            await interaction.response.send_message("Profile not found. Please add profile to use this command")
        else: 
            userdata = db.getUserData(user)
            if userdata is not None:
                _, charactername, region, realm = userdata   
                string_return = api.GetLowestKey(region, realm, charactername)
                await interaction.response.send_message(f'The lowest keys of **{charactername}** are: \n {string_return}')    

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(rio_commands(bot))