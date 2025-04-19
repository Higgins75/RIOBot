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

class profile_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Adds a user profile to the database
    @discord.app_commands.command(name="add_profile", description="Add your user profile")
    async def add_profile(self, interaction: discord.Interaction, region: Literal[regions], realm: str, charactername: str):
        user = str(interaction.user)
        db.insertProfile(user, charactername, region, realm)
        RaiderLinkURL = api.GetRioLink(region, realm, charactername)
        await interaction.user.send(f"Linked your DiscordID to the profile for {RaiderLinkURL}")
        await interaction.response.send_message(f"User Profile added")
        
    # Deletes user data from the database    
    @discord.app_commands.command(name="delete_profile", description="Delete your user profile")
    async def delete_profile(self, interaction: discord.Interaction):
        user = str(interaction.user)
        return_string = db.removeProfile(user)
        await interaction.response.send_message(f'{return_string}')

    # Checks a user has a profile in the SQLite Database, returns associated character name   
    @discord.app_commands.command(name="check_profile", description="Check if your profile exists")  
    async def check_profile(self, interaction: discord.Interaction):
        user = str(interaction.user)   
        if db.checkUserExists(user):
            userdata = db.getUserData(user)
            _, charactername, _, _ = userdata
            await interaction.response.send_message(f'Profile found for {charactername}')
        else:
            await interaction.response.send_message("Profile not found")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(profile_commands(bot))