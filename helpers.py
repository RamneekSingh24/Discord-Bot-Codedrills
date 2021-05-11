import requests
from bs4 import BeautifulSoup
import discord
import os
import pandas as pd

import weasyprint as wsp
import PIL as pil


def get_url(task,handle):
  URL = 'https://recommender.codedrills.io/profile?handles=cf%2Fjatinmunjal2k'
  page = requests.get(URL)

  soup = BeautifulSoup(page.content, 'html.parser')
  
  # print(task)
  
  result = soup.find(id=task)

  url = result.find(title='An url for sharing and keeping track of solved problems for this recommendation list')
  link = "https://recommender.codedrills.io"+url['href']
  return link

def get_problems(task, ID,handle):
  # print(ID)
  items = [[],[]]
  buffer = ""
  URL = get_url(task,handle)
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  elems = soup.find_all('tr')
  idx = 1
  for e in elems:
    a_tag = e.find('a')
    buffer = buffer +"["+str(idx)+"](" + a_tag['href'] + ") " + a_tag.text + "\n"
    items[0].append(a_tag.text)
    items[1].append(a_tag['href'])
    idx += 1

  df = pd.DataFrame(list(zip(items[0],items[1])), columns = ['name', 'link'])
  df.to_csv('contests/problems-contest'+str(ID)+'.csv' , index = False)
  #print(df.head(3))

  return buffer

def load_problems(id):
  df = pd.read_csv('contests/problems-contest'+str(id)+'.csv')
  buffer = ""
  for idx, row in df.iterrows():
    buffer = buffer + row['name'] + " [Link](" + row['link'] + ")\n"
  return buffer
  

def trim(source_filepath, target_filepath=None, background=None):
    if not target_filepath:
        target_filepath = source_filepath
    img = pil.Image.open(source_filepath)
    if background is None:
        background = img.getpixel((0, 0))
    border = pil.Image.new(img.mode, img.size, background)
    diff = pil.ImageChops.difference(img, border)
    bbox = diff.getbbox()
    img = img.crop(bbox) if bbox else img
    img.save(target_filepath)

