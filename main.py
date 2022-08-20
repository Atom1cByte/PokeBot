import os
import discord
from config import *
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="p!", intents=intents)

extensions = []

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        extensions.append("cogs."+filename[:-3])

if __name__ == "__main__":
    for ext in extensions:
        client.load_extension(ext)

client.run(TOKEN)