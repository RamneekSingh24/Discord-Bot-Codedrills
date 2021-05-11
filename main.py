import requests
from bs4 import BeautifulSoup
import discord
import os
from tabulate import tabulate
import handlers
import pandas as pd
from helpers import get_url, get_problems, trim,load_problems
from handlers import start_contest, update_leaderboard,add_cf_user,users,get_recommendations_topics, set_handle, recommendations_handle

from keep_alive import keep_alive

import weasyprint as wsp
import PIL as pil

# global running
# running = contest_running



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  global contest_running

  if message.author == client.user:
      return

  msg = message.content
  #params = msg.lower().split(' ')
  params = msg.split(' ')
  if params[0][0] != '!':
    return

  if params[0] == '!setrc':
    handle = params[1]
    rc = set_handle(handle)
    if rc < 0:
      await message.channel.send('Invalid codeforces handle')
    else:
      await message.channel.send('Done! Getting recommandations from: '+handle+".")

  
  if params[0] == '!topics':
    msg = get_recommendations_topics(recommendations_handle)
    await message.channel.send(msg)

  if params[0] == '!add':
    username = params[1]
    rc = add_cf_user(username)
    if rc == -1:
      await message.channel.send('User already registered!')
    elif rc == -2:
      await message.channel.send('Not a valid user on CodeForces!')
    else:
      await message.channel.send(f"Sucessfully added {username}")

  elif params[0] == '!all':
    await message.channel.send(users)

  elif params[0] == '!start':
    if handlers.contest_running:
      await message.channel.send("A contest is already Active !")
      return
    task = "_".join(word for word in params[1:])
    #img_filepath = 'table.png'
    #print(task)
    msg = start_contest(task)
    
    if msg == "error":
      await message.channel.send("Please Try Again!")
    else: 
      e = discord.Embed(
        title=f"Problem Set {handlers.ID}\n",
        description=msg,
        color=0xFF5733)
      await message.channel.send(embed=e)

  elif params[0] == '!lb':
    id = params[1] if len(params) > 1 else handlers.ID
    df_lead = update_leaderboard(id)
    df_lead['Total'] = df_lead[list(df_lead.columns)[1:]].sum(axis=1)
    df_lead.sort_values(by='Total',ascending=False, inplace=True)
    await message.channel.send("```"+tabulate(df_lead, headers='keys', tablefmt='psql', showindex=False)+"```")
    # f = discord.File('table.png', filename="image.png")
    # e = discord.Embed(title='Leaderboard', color=0xFF5733)
    # e.set_image(url="attachment://image.png")
    # await message.channel.send(file=f, embed=e)
  
  elif params[0] == "!prob":
    id = params[1] if len(params) > 1 else handlers.ID
    msg = load_problems(id)
    e = discord.Embed(
      title=f"Problem Set {handlers.ID}\n",
      description=msg,
      color=0xFF5733)
    await message.channel.send(embed=e)

  elif params[0] == "!end":
    if handlers.contest_running == 0:
      await message.channel.send("No contest is running !")
    else:
      handlers.contest_running = 0
      await message.channel.send("Contest Abandoned !")

keep_alive()
client.run(os.getenv('TOKEN'))
