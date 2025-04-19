#Python Lib imports
import os
import asyncio

#discord.py import
import discord
from discord.ext import commands

#Get Token from ENV File
from dotenv import load_dotenv
load_dotenv()
bot_token = os.getenv("token")


#Sets up Discord
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.',intents=intents)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(bot_token)

@bot.event
async def on_ready():
    # Print total loaded commands
    total_slash_commands = len(bot.tree.get_commands())
    total_prefix_commands = len(bot.commands)

    print(f"🤖 Bot is ready as {bot.user}")
    print(f"🌐 Slash Commands Loaded: {total_slash_commands}")
    print(f"⌨️ Prefix Commands Loaded: {total_prefix_commands}\n")

if __name__ == "__main__":
    asyncio.run(main())
