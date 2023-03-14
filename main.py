from http import client
import os
import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from datetime import datetime
from translate import Translator
from python_aternos import Status
import python_aternos




intents = discord.Intents.all()
client = commands.Bot(command_prefix="m!", intents = intents)
aternos = python_aternos.Client.from_credentials('SamCooper', 'coop@aternoslol')
token = (os.environ["DISCORD_TOKEN"])




@client.event
async def on_ready():
    game = discord.Game("with the crew.")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('Online as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Try again in {round(error.retry_after)} seconds.')







@client.command()
async def translate(ctx, from_lang, to_lang):
    translator= Translator(to_lang=to_lang, from_lang=from_lang, secret_access_key=None, base_url='https://translate.astian.org/')
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    translation = translator.translate(str((message.content)))
    await ctx.send(str(translation))

@client.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def minecraft(ctx):
    servs = aternos.list_servers()
    cre = servs[0]
    sur = servs[1]
    status_emote = lambda x : "🟢" if x == "online" else "🔴"
    embed = discord.Embed(title="Arrgh's minecraft servers.", description=f'''
**Creative** : {cre.status}  {status_emote(cre.status)}
{cre.players_count} player/s active.
**Players** : ``{cre.players_list}``

**Survival** : {sur.status}  {status_emote(sur.status)}
{sur.players_count} player/s active.
**Players** : ``{sur.players_list}``
    ''')
    await ctx.send(embed = embed)



@client.command()
@commands.cooldown(1, 150, commands.BucketType.guild)
async def minestart(ctx, server_type):
    servs = aternos.list_servers()
    if server_type in ["creative", "survival"]:
        servers = {"creative": servs[0], "survival":servs[1]}
        server = servers[server_type]
        try:
            server.start()
            await ctx.send("server is starting, check in about 2 minutes.")
        except:
            await ctx.send("there was an error, make sure server is not already online or ping sam to manually start the server.")






client.run(token)