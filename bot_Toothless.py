#######################################################################################################################################
##Toothless
import asyncio
import functools
import itertools
import math
import random
import asyncpg

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions , Bot
from itertools import cycle

###########################################-----Bot Initialisation-----#######################################################

bot = commands.Bot(command_prefix = "")
###########################################-----Events-----####################################################################

async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database = "Discord_test", user ="postgres", password = "Dheeru@1612")

import os
for cog in os.listdir(os.path.abspath("Cogs")):
    if cog.endswith(".py"):
        try:
            cog = f"Cogs.{cog.replace('.py','')}"
            bot.load_extension(cog)
            print("Loaded ",cog)
        
        except Exception as e:
            print(f"{cog} cannot be loaded")
            raise e

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle , activity = discord.Game("Havana"))
    print("Bot is ready")
    change_status.start() #background task

#############################################-----Reminders-----#################################################
'''
@bot.command(name = "remind", pass_context = True)
async def remind( ctx ):
    getTime()
    args = ctx.message.content
    args = args.split(' ')
    try:
        if('s' in args[2]):
            time = int(args[2].replace('s',' '))
            await ctx.send(f"Will remind in {str(args[2].replace('s',' '))} to {str(args[1])}")
            await asyncio.sleep(time)
            await ctx.send(ctx.message.author,f"You asked me to remind to {str(args[1])} {str(time)} seconds from {str(getTime())}")
    except:
        pass
'''
#############################################-----Background tasks-----###############################################
# must import itertools(cycle) and discord.ext (tasks)

status=cycle(["Senorita","Bad Things","Havana"])

@tasks.loop(seconds=300)
async def change_status():
    await bot.change_presence(activity = discord.Game(next(status)))

bot.loop.run_until_complete(create_db_pool())

bot.run("NzE3MzkyNzIwMTA0MjU5NjE0.XtZqLg.ChRLy7LuhArMNo2bNLenkZq2LYs")
