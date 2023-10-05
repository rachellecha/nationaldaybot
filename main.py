# import libraries
import os
from dotenv import load_dotenv

#discord stuff
import discord
from discord.ext import tasks, commands

#datetime import
import datetime

#functions to actually do the work
from modules import updateHolidays, summ


#environment variables
load_dotenv()
TOKEN = os.getenv('DISC_TOKEN')
CHANNEL = os.getenv('DISC_CHANNEL')

#create the discord bot
intents = discord.Intents.default()
intents.message_content = True

#time the message will send
#utc is default #10AM EST
messageTime = datetime.time(hour=14) 
bot = commands.Bot(command_prefix='!', intents=intents)


#method to send all the holidays in discord channel at the specified time
@tasks.loop(time=messageTime)
async def NationalDaySend():
    channel = bot.get_channel(int(CHANNEL))
    print(channel)
    days = updateHolidays()
    embed = discord.Embed(title="Here Are The Fun Holidays For Today")
    for holiday in days:
        embed.add_field(name='\n', value=f'{holiday}\n', inline=False)
    await channel.send(embed=embed)
    print('working!!')

#runs when the client runs
@bot.event
async def on_ready():
    if not NationalDaySend.is_running():
        NationalDaySend.start()
        print("started")

@bot.command(pass_context=True)
async def tldr(ctx, arg):
    channel = bot.get_channel(int(CHANNEL))
    messages = [message async for message in channel.history(limit=int(arg))]
    convo = []
    for i in messages:
        convo.append(i.content)
    result = summ(convo)
    await channel.send(result)

bot.run(TOKEN) 