from http import client
from TOKEN import TOKEN
import discord
import asyncio


client = discord.Client()
client.run(TOKEN)