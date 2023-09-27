# bot.py
import os
from test import updateHolidays

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

messageTime = datetime.time(hour=14) #utc is default #10AM EST

@tasks.loop(time=messageTime)
async def NationalDaySend():
    #print('here')
    channel = client.get_channel(int(CHANNEL))
    print(channel)
    days = updateHolidays()
    #await channel.send(f"## Here are the holidays for today!  \n **{days[0]} \n {days[1]} \n {days[2]}**")
    embed = discord.Embed(title="Here Are The Fun Holidays For Today")
    for holiday in days:
        embed.add_field(name='\n', value=f'{holiday}\n', inline=False)
    await channel.send(embed=embed)
    print('working!!')

@client.event
async def on_ready():
    if not NationalDaySend.is_running():
        NationalDaySend.start()
        print("started")

 
client.run(TOKEN)