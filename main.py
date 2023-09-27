# import libraries
import os
from dotenv import load_dotenv

#discord stuff
import discord
from discord.ext import tasks

#datetime import
import datetime

#functions to actually do the work
from modules import updateHolidays


#environment variables
load_dotenv()
TOKEN = os.getenv('DISC_TOKEN')
CHANNEL = os.getenv('DISC_CHANNEL')
#print(CHANNEL)

#create the discord bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#time the message will send
#utc is default #10AM EST
messageTime = datetime.time(hour=14) 


#method to send all the holidays in discord channel at the specified time
@tasks.loop(time=messageTime)
async def NationalDaySend():
    channel = client.get_channel(int(CHANNEL))
    #print(channel)
    days = updateHolidays()
    embed = discord.Embed(title="Here Are The Fun Holidays For Today")
    for holiday in days:
        embed.add_field(name='\n', value=f'{holiday}\n', inline=False)
    await channel.send(embed=embed)
    #print('working!!')

#runs when the client runs
@client.event
async def on_ready():
    if not NationalDaySend.is_running():
        NationalDaySend.start()
        #print("started")

 
client.run(TOKEN)