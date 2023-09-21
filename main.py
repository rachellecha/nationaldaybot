# bot.py
import os
from test import dayGenerator

import discord
from dotenv import load_dotenv
from discord.ext import tasks
import datetime

load_dotenv()
TOKEN = os.getenv('DISC_TOKEN')
CHANNEL = os.getenv('DISC_CHANNEL')
print(CHANNEL)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

messageTime = datetime.time(hour=3, minute=39)

@tasks.loop(time=messageTime)
async def NationalDaySend():
    print('here')
    channel = client.get_channel(1154241704430415893)
    print(channel)
    days = dayGenerator()
    await channel.send(days)
    print('working!!')

@client.event
async def on_ready():
    if not NationalDaySend.is_running():
        NationalDaySend.start()
        print("started")

 
client.run(TOKEN)