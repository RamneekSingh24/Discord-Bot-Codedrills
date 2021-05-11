import requests
from bs4 import BeautifulSoup
import discord
import os
from tabulate import tabulate
import pandas as pd
from helpers import get_url, get_problems, trim,load_problems
from keep_alive import keep_alive

import weasyprint as wsp
import PIL as pil

global ID, contest_running, users, recommendations_handle
ID = 0
contest_running = 0
users = []
recommendations_handle = 'jatinmunjal2k'



def get_recommendations_topics(handle='jatinmunjal2k'):
  topics = "Available Topics:\n"
  URL = 'https://recommender.codedrills.io/profile?handles=cf%2F' + handle
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  ul = soup.find("ul", class_="nav nav-pills")
  tags = ul.find_all('li')
  for e in tags:
    topics = topics + e.text.strip() + ", "
  return topics[:-2]


def set_handle(handle):
  global recommendations_handle
  r = requests.head('https://codeforces.com/profile/'+handle)
  if r.status_code != 200:
    return -1
  recommendations_handle = handle
  return 0

def start_contest(task):
  global ID, contest_running
  try:
    ID += 1
    problems_str = get_problems(task, ID,recommendations_handle)
    init_leaderboard(ID)
    contest_running = 1
    return problems_str
  except:
    ID -= 1
    return "error"
    
def add_cf_user(cf_handle):
  global users

  if cf_handle in users:
    return -1

  r = requests.head('https://codeforces.com/profile/'+cf_handle)
  if r.status_code != 200:
    return -2

  users.append(cf_handle)
  if contest_running == 1:
    df = pd.read_csv('contests/leaderboard'+str(ID)+'.csv')
    entry = [cf_handle] + [0]*(df.shape[1]-1)
    df.loc[len(df)] = entry
    df.to_csv('contests/leaderboard'+str(ID)+'.csv',index = False)

  return 1

# def print_leaderboard(id, img_filepath):
#   df_leaderboard = pd.read_csv('contests/leaderboard'+str(id)+'.csv')
#   css = wsp.CSS(string='''
#   @page { size: 2048px 2048px; padding: 0px; margin: 0px; }
#   table, td, tr, th { border: 1px solid black; }
#   td, th { padding: 4px 8px; }
#   ''')
#   html = wsp.HTML(string=df_leaderboard.to_html(index=False))
#   html.write_png(img_filepath, stylesheets=[css])
#   trim(img_filepath)

def init_leaderboard(id):
  df = pd.read_csv('contests/problems-contest'+str(id)+'.csv')
  problems = df['name']
  zeros = [ [0]*len(users) for i in range(len(problems))]
  df_scoreboard = pd.DataFrame(data=list(zip(users,*zeros)), columns=['User']+list(range(1,len(problems)+1)))
  df_scoreboard.to_csv('contests/leaderboard'+str(id)+'.csv',index=False)
  
  # print_leaderboard(id, img_filepath)
  

def update_leaderboard(id):
  global users
  df_prob = pd.read_csv('contests/problems-contest'+str(id)+'.csv')
  df_lead = pd.read_csv('contests/leaderboard'+str(id)+'.csv')

  for idxu, ru in df_lead.iterrows():
    user = ru['User']
    URL = 'https://codeforces.com/submissions/' + user
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    submissions = soup.find_all('tr')
    ac = []
    for submission in submissions:
        data = submission.find_all('td')
        try:
          url = data[3].find('a')['href'].split('/')
          verdict = data[5].text
          #print(url, repr(verdict))
          if 'Accepted' in verdict:
            ac.append('/'+url[2]+'/'+url[-1])
        except:
          continue
          
    j = 0
    for idx, row in df_prob.iterrows():
      j += 1
      link = row['link']
      for pid in ac:
        if pid in link:
          df_lead.at[idxu,str(j)] = 1

  df_lead.to_csv('contests/leaderboard'+str(id)+'.csv',index = False)
  # print_leaderboard(id, 'table.png')
  return df_lead


#add_cf_user('jatinmunjal2k')
# add_cf_user('chill_coder')
#update_leaderboard(1)



# client = discord.Client()

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))


# @client.event
# async def on_message(message):
#     global contest_running

#     if message.author == client.user:
#         return

#     msg = message.content
#     params = msg.lower().split(' ')
#     if params[0][0] != '!':
#       return

#     if params[0] == '!add':
#       username = params[1]
#       rc = add_cf_user(username)
#       if rc == -1:
#         await message.channel.send('User already registered!')
#       elif rc == -2:
#         await message.channel.send('Not a valid user on CodeForces!')
#       else:
#         await message.channel.send(f"Sucessfully added {username}")

#     elif params[0] == '!all':
#       await message.channel.send(users)

#     elif params[0] == '!start':
#       if contest_running:
#         await message.channel.send("A contest is already Active !")
#         return
#       task = params[1][0].upper()+params[1][1:]
#       img_filepath = 'table.png'
#       msg = start_contest(task, img_filepath)
#       # await message.channel.send(f"Problem Set {ID}\n")
#       # await message.channel.send("```"+msg+"```")
#       e = discord.Embed(
#         title=f"Problem Set {ID}\n",
#         description=msg,
#         color=0xFF5733)
#       await message.channel.send(embed=e)

#     elif params[0] == '!lb':
#       id = params[1] if len(params) > 1 else ID
#       df_lead = update_leaderboard(id)
#       df_lead['Total'] = df_lead[list(df_lead.columns)[1:]].sum(axis=1)
#       df_lead.sort_values(by='Total',ascending=False, inplace=True)
#       await message.channel.send("```"+tabulate(df_lead, headers='keys', tablefmt='psql', showindex=False)+"```")
#       # f = discord.File('table.png', filename="image.png")
#       # e = discord.Embed(title='Leaderboard', color=0xFF5733)
#       # e.set_image(url="attachment://image.png")
#       # await message.channel.send(file=f, embed=e)
    
#     elif params[0] == "!prob":
#       id = params[1] if len(params) > 1 else ID
#       msg = load_problems(id)
#       e = discord.Embed(
#         title=f"Problem Set {ID}\n",
#         description=msg,
#         color=0xFF5733)
#       await message.channel.send(embed=e)

#     elif params[0] == "!end":
#       if not contest_running:
#         await message.channel.send("No contest is running !")
#       else:
#         contest_running = 0
#         await message.channel.send("Contest Abandoned !")

# keep_alive()
# client.run(os.getenv('TOKEN'))
