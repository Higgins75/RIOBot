import discord
from typing import Literal
from discord.ext import commands
from Bot_Token import token
from API_Call import GetRioLink

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='.',intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")
    
@bot.tree.command(name="raidlink")
async def raiderurl(interaction: discord.Interaction, region : Literal['eu', 'na'], realm: str, charactername: str):
    RaiderLinkURL = GetRioLink(region, realm, charactername)
    await interaction.response.send_message(f'Your RIO link is {RaiderLinkURL}')
        
bot.run(token)