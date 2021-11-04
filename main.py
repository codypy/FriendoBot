import discord
import os
import random
import requests
import json
from replit import db
from keep_alive import keep_alive

# iniitializing discord client
client = discord.Client()

# initial list of words they are overwritten and saved into data base when user adds new words
starter_sadwords = ['sad', 'alone']
encourage_starter = ['nice', 'dont be sad', 'you are doing great', 'pick your head up', 'confucious say no sad', 'big booty bitches']

# getting inspiring quote
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# function to update encouragements
def update_encourage(args):
    if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        encouragements.append(args)
        db['encouragements'] = encouragements
    else:
        global encourage_starter
        encourage_starter.append(args)
        db['encouragements'] = encourage_starter

# to delete encouragements
def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements

# function to update sad words
def update_sadwords(args):
    if 'sadwords' in db.keys():
        sadwords = db['sadwords']
        sadwords.append(args)
        db['sadwords'] = sadwords
    else:
        global starter_sadwords
        starter_sadwords.append(args)
        db['sadwords'] = starter_sadwords

# to delete sadwords
def delete_sadword(index):
  sadwords = db['sadwords']
  if len(sadwords) > index:
    del sadwords[index]
    db['sadwords'] = sadwords

@client.event
async def on_ready():
    print(f'i am ready {client.user}')


@client.event
async def on_message(message):
    # if msg is sent by bot itself then ignore
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    # if msg contain pre-defined words reply it with the pre-defined phrase
    if msg.startswith('!hello'):
        await message.channel.send('Hello')

    # if any words from msg is in the sad words list then send any random msg from encouragements
    if any(word in msg for word in starter_sadwords):
        await message.channel.send(random.choice(encourage_starter))

    # if msg starts with '!newEnco' means user want to add new encouragements
    if msg.startswith('!new'):
        new = msg.split('!new ', 1)[1]
        update_encourage(new)
        await message.channel.send(f'new "{new}" encouragement is added!')

    # to list encouragements 
    if msg.startswith('!list'):
        encouragements = []
        if 'encouragements' in db.keys():
            encouragements = db['encouragements']
            if len(encouragements) == 0:
              await message.channel.send('The list is empty please add new encouragements by command "!new"')
            else:
              list1 = '\n'.join(encouragements)
        await message.channel.send(list1)

    # to delete encouragements
    if msg.startswith('!delete'):
      encouragements = []
      if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        index = int(msg.split('!delete ',1)[1])
        index = index - 1
        delete_encouragement(index)
        await message.channel.send('Encouragements is deleted')

    # if msg starts with '!newSad' means user want to add new sad word
    if msg.startswith('!newSad'):
        new = msg.split('!newSad ', 1)[1]
        update_sadwords(new)
        await message.channel.send(f'new sad "{new}"word added')

    # to list sadwords
    if msg.startswith('!listSad'):
        sadwords = []
        if 'sadwords' in db.keys():
            sadwords = db['sadwords']
            if len(sadwords) == 0:
              await message.channel.send('the list is empty')
            else:
              lost = '\n'.join(sadwords)
        await message.channel.send(lost)

        # if len(db['sadwords']) == 0:
        #   await message.channel.send('The list is empty please add new sad words')
        

    # to delete sadwords
    if msg.startswith('!deleteSad'):
      sadowrds = []
      if 'sadwords' in db.keys():
        sadwords = db['sadwords']
        index = int(msg.split('!deleteSad ',1)[1])
        index = index - 1
        delete_sadword(index)
        await message.channel.send('sadowrd is deleted')

keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)