from util.saveTournaments import saveTournaments
from util.getTournamentList import getTournamentList
from util.getDateAndTime import getDateAndTime
from util.getTournamentJSON import getTournamentJSON
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands, tasks
import time
import asyncio
from datetime import datetime, timezone

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWTV_URL = os.getenv("OWTV_URL")
PREFIX = os.getenv("GLOBAL_PREFIX")
FETCH_TOURNAMENT_ERR = 'Failed to fetch tournaments.'
pages = ['/matches', '/tournaments', '/news']
tournamentDataJson = getTournamentJSON() # json data from tournaments page, use this for all tournament related commands/methods

intents = discord.Intents.default()
intents.message_content = True
owtvBot = commands.Bot(command_prefix=PREFIX, intents=intents)

@owtvBot.event # a decorator, tells the discord.py library that the following function is an event handler (in this case, handling the "on_ready" event)
async def on_ready():
    print("OWTV.gg Bot online!")
    await tournamentLoader.start()

@tasks.loop(minutes=10)
async def tournamentLoader():
    try:
        print('Fetching tournaments...')
        await saveTournaments(OWTV_URL, pages[1])
    except Exception as e:
        print(f'{FETCH_TOURNAMENT_ERR}: {e}')
        tournamentLoader.stop()

@owtvBot.command(name="tournaments") # "!tournaments" : sends an embedded msg of the currently listed tournaments on OWTV.gg/tournaments (flags to be added)
async def tournaments(ctx):
    tournaments = getTournamentList(tournamentDataJson)
    
    if not tournaments:
        await ctx.send("No tournaments found right now.")
        return
    
    # create the tournaments message as an embed (it's prettier)
    embed = discord.Embed(
        title="Tournaments",
        description="Tournament list", # to be changed to match respective flags
        color=discord.Color.blue(),
        timestamp=datetime.now(timezone.utc)
    )

    for t in tournaments:
        name = t.split('\n')[0] # get the first element in the split index (since it is always the tournament name)
        link = OWTV_URL.format(t.split(':')[1])
        embed.add_field(name=name, value=f'[View]({link})', inline=False)

    embed.set_footer(text=f'Data from OWTV.gg | OWCS Logo from Liquipedia.net')
    embed.set_thumbnail(url='https://github.com/chezecakes/owcs-thingy/blob/main/data/images/OWCS_Logo_Transparent.png?raw=true')

    await ctx.send(embed=embed)

@owtvBot.command(name="test") # command for testing
async def test(ctx):
    ctx.send('<:pacific:1417219343128723627>\n<:na:1417219329287524586>\n<:korea:1417219320769024050>\n<:japan:1417219312133083333>\n<:emea:1417219294093115523>\n<:china:1417219278595428362>\n<:asia:1417219268558323833>')

owtvBot.run(BOT_TOKEN)