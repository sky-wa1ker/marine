from http import client
import os
import discord
from discord.ext import commands, tasks
import re
import json
from datetime import datetime
from translate import Translator
import time



intents = discord.Intents.all()
client = commands.Bot(command_prefix="m!", intents = intents)
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
@commands.cooldown(1, 10, commands.BucketType.user)
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')


@client.command()
async def translate(ctx, from_lang, to_lang):
    translator= Translator(to_lang=to_lang, from_lang=from_lang, secret_access_key=None, base_url='https://translate.astian.org/')
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    translation = translator.translate(str((message.content)))
    await ctx.send(str(translation))



client.run(token)