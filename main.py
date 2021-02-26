import discord
import secrets
import itertools
import random
import re
import os
from keepAlive import keep_alive
import requests
import json

client = discord.Client()
prefix = '&'

diceTypes = [4,6,8,10,12,20,100]

dnd5e_races = ["DragonBorn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfing", "Half-Orc", "Human", "Tiefling", "Orc of Exandria", "Leonin", "Satyr", "Aarakocra", "Genasi", "Goliath", "Aasimar", "Bugbear", "Firbolg", "Goblin", "Hobgoblin", "Kenku", "Kobold", "Lizardfolk", "Orc", "Tabaxi", "Triton", "Yuan-ti Pureblood", "Feral Tiefling", "Tortle", "Changeling", "Kalashtar", "Orc of Eberron", "Shifter", "Warforged", "Gith", "Centaur", "Loxodon", "Minotaur", "Simic Hybrid", "Vedalken", "Verdan", "Locatah", "Grung"]

dnd5e_races_phb = ["DragonBorn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfing", "Half-Orc", "Human", "Tiefling"]

dnd5e_classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Walorck", "Wizard", "Artificer", "Blood Hunter"]

dnd5e_classes_phb = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Walorck", "Wizard"]

def searchCondition(query):
  response = requests.get('https://www.dnd5eapi.co/api/conditions/'+query)
  json_data = json.loads(response.text)
  name = json_data['name']
  desc = ''
  for i in json_data['desc']:
    desc = desc + i+"\n"
  return (name,desc)

def conditionList():
  response = requests.get('https://www.dnd5eapi.co/api/conditions')
  json_data = json.loads(response.text)
  cond = ''
  for i in json_data['results']:
    cond = cond + i['index']+", "
  return cond[:-2]
    

def searchAbility(query):
  response = requests.get('https://www.dnd5eapi.co/api/ability-scores/'+query)
  json_data = json.loads(response.text)
  name = json_data['name']
  desc = ''
  for i in json_data['desc']:
    desc = desc + i+"\n"
  skills = ''
  for i in json_data['skills']:
    skills = skills + i['name'] + ", "
 
  return (name,desc,skills[:-2])

def abilityList():
  response = requests.get('https://www.dnd5eapi.co/api/ability-scores')
  json_data = json.loads(response.text)
  cond = ''
  for i in json_data['results']:
    cond = cond + i['index']+", "
  return cond[:-2]

def skillList():
  response = requests.get('https://www.dnd5eapi.co/api/skills')
  json_data = json.loads(response.text)
  cond = ''
  for i in json_data['results']:
    cond = cond + i['index']+", "
  return cond[:-2]

def searchSkill(query):
  response = requests.get('https://www.dnd5eapi.co/api/skills/'+query)
  json_data = json.loads(response.text)
  name = json_data['name']
  desc = ''
  for i in json_data['desc']:
    desc = desc + i+"\n"
  abi = json_data['ability_score']['index']
  return (name,desc,abi)

def damageList():
  response = requests.get('https://www.dnd5eapi.co/api/damage-types')
  json_data = json.loads(response.text)
  damage = ''
  for i in json_data['results']:
    damage = damage + i['index']+", "
  return damage[:-2]

def searchDamage(query):
  response = requests.get('https://www.dnd5eapi.co/api/damage-types/'+query)
  json_data = json.loads(response.text)
  name = json_data['name']
  desc = ''
  for i in json_data['desc']:
    desc = desc + i+"\n"
  return (name,desc)

def helpList():
  string = '**Praise Asmodeus**'+'\n'+'Bot prefix: '+ prefix + '\n' + 'Rolling Dice: &[#dice]d[Type], ex: &8d6' + '\n' + 'Random Race(w/Expansions): &randrace' + '\n' + 'Random Race(PHB): &randracephb'+ '\n' + 'Random Class(w/Expansions): &randclass' + '\n' + 'Random Class(PHB): &randclassphb' + '\n' + 'Random Ability Scores: &randas'+ '\n' + 'Roll d20 with advantage: &adv' + '\n' + 'Roll d20 with disadvantage: &ddv' + '\n' + 'Roll 1d20: &r' + '\n' + 'Generate Random Character(w/Expansions): &randchar' + '\n' + 'Generate Random Character(PHB): &randcharphb' + '\n' + 'Ability Scores List: &abi' + '\n' + 'Ability Scores Descriptions: &[ability], ex:&dex' + '\n' + 'Conditions List: &cond' + '\n' + 'Conditions Description: &[condition], ex: &exhaustion' + '\n' + 'Skills List: &skills' + '\n' + 'Skills Description: &[skill], ex:&animal-handling' + '\n' + 'Damage Types: &damage' + '\n' + 'Damage Types Description: &[type], ex: &thunder'

  return string


def diceRoll(message):
  split = re.split('&|d',message)
  number = int(split[1])
  dice = int(split[2])
  string = ''
  result = 0
  if dice in diceTypes:
    if number == 1:
      rand = random.randrange(1, dice+1)
      result = rand
      string = string + str(rand)
    else:
      for i in itertools.repeat(None, number):
        rand = random.randrange(1, dice+1)
        result = result + rand
        string = string + str(rand) + ', '

  else:
    string = 'Invalid'
    result = dice

  return (string[:-2],result)

def randAS():
  string = ''
  ability = 0
  total = 0
  for i in itertools.repeat(None, 6):
    one =  random.randrange(1, 7) 
    two = random.randrange(1, 7)  
    three = random.randrange(1, 7) 
    four = random.randrange(1, 7)
    list = [one, two, three, four]
    list2 = '('
    lowest = min(list)
    ability = sum(list) - lowest
    total = total + ability
    counter = 0
    for i in list:
      counter = counter + 1
      if i != lowest and counter == 4:
        list2 = list2 + ' '+ str(i) + ' )' 
      if i != lowest and counter != 4:
        list2 = list2 + ' '+str(i) + ' ,'
      if i == lowest and counter == 4:
        list2 = list2 + ' '+'~~'+str(i)+'~~' + ' )'
        lowest = 0
      if i == lowest and counter != 4:
        list2 = list2 + ' '+'~~'+str(i)+'~~' + ' ,'
        lowest = 0
    string = string + list2 + ' = '+'**'+str(ability)+'**'+ "\n" 
  return string + 'Total: ' + '**'+str(total)+'**'
  

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if re.fullmatch(prefix+r'\d*d\d*',message.content):
    (string,result) = diceRoll(message.content)
    if string == 'Invalid':
      await message.channel.send(message.author.mention +"\n"+'Invalid dice format: d'+str(result))
    else:
      await message.channel.send( message.author.mention +"\n"+ '**Rolls:** '+ string +"\n"+ '**Total:** '+ str(result) )

  if re.fullmatch(prefix+r'randrace',message.content):
    racechoice = secrets.choice(dnd5e_races)
    await message.channel.send(message.author.mention +"\n"+racechoice)

  if re.fullmatch(prefix+r'randracephb',message.content):
    classchoice = secrets.choice(dnd5e_races_phb)
    await message.channel.send(message.author.mention +"\n"+classchoice)

  if re.fullmatch(prefix+r'randclass',message.content):
    racechoice = secrets.choice(dnd5e_classes)
    await message.channel.send(message.author.mention +"\n"+racechoice)

  if re.fullmatch(prefix+r'randclassphb',message.content):
    classchoice = secrets.choice(dnd5e_classes_phb)
    await message.channel.send(message.author.mention +"\n"+classchoice)

  if re.fullmatch(prefix+r'randas',message.content):
    await message.channel.send(message.author.mention +"\n"+randAS())

  if re.fullmatch(prefix+r'adv',message.content):
    rand = random.randrange(1, 21)
    rand2 = random.randrange(1, 21)
    if rand > rand2:
      rand = '**'+str(rand)+'**'
      rand2 = str(rand2)
    else:
      rand = str(rand)
      rand2 = '**'+str(rand2)+'**'

    await message.channel.send(message.author.mention +"\n"+'**Advantage Rolls:** '+ rand+ ', ' + rand2 )

  if re.fullmatch(prefix+r'ddv',message.content):
    rand = random.randrange(1, 21)
    rand2 = random.randrange(1, 21)
    if rand < rand2:
      rand = '**'+str(rand)+'**'
      rand2 = str(rand2)
    else:
      rand = str(rand)
      rand2 = '**'+str(rand2)+'**'

    await message.channel.send(message.author.mention +"\n"+'**Disadvantage Rolls:** '+ rand+ ', ' + rand2 )

  if re.fullmatch(prefix+r'r',message.content):
    rand = random.randrange(1, 21)
    await message.channel.send(message.author.mention +"\n"+'**Roll:** ' +  str(rand))

  if re.fullmatch(prefix+r'randchar',message.content):
    racechoice = secrets.choice(dnd5e_races)
    classchoice = secrets.choice(dnd5e_classes)
    await message.channel.send(message.author.mention +"\n" +'**Race:** '+"\n"+racechoice+"\n"+'**Class:** '+classchoice + "\n" +'**Ability Scores:** ' +"\n" +randAS())

  if re.fullmatch(prefix+r'randcharphb',message.content):
    racechoice = secrets.choice(dnd5e_races_phb)
    classchoice = secrets.choice(dnd5e_classes_phb)
    await message.channel.send(message.author.mention +"\n" +'**Race:** '+"\n"+racechoice+"\n"+'**Class:** '+classchoice + "\n" +'**Ability Scores:** ' +"\n" +randAS())

  if re.fullmatch(r'&blinded|&charmed|&deafened|&exhaustion|&frightened|&grappled|&incapacitated|&invisible|&paralyzed|&petrified|&poisoned|&restrained|&stunned|&unconscious',message.content):
    (name,desc)=searchCondition(message.content[1:])
    await message.channel.send(message.author.mention +"\n" +'**Name:** '+name+"\n"+'**Desc:** '+desc)

  if re.fullmatch(r'&str|&con|&dex|&wis|&cha|&int',message.content):
    (name,desc,skills)=searchAbility(message.content[1:])
    await message.channel.send(message.author.mention +"\n" +'**Name:** '+name+"\n"+'**Desc:** '+desc+"\n"+'**Skills:** '+skills)

  if re.fullmatch(prefix+r'cond',message.content):
    cond = conditionList()
    await message.channel.send(message.author.mention +"\n" +'**Conditions:** '+cond)
  
  if re.fullmatch(prefix+r'abi',message.content):
    abi = abilityList()
    await message.channel.send(message.author.mention +"\n" +'**Ability Scores:** '+abi)

  if re.fullmatch(prefix+r'skills',message.content):
    skill = skillList()
    await message.channel.send(message.author.mention +"\n" +'**Skills:** '+skill)

  if re.fullmatch(r'&acrobatics|&animal-handling|&arcana|&athletics|&deception|&history|&insight|&intimidation|&investigation|&medicine|&nature|&perception|&performance|&persuasion|&religion|&sleight-of-hand|&stealth|&survival',message.content):
    (name,desc,abi)=searchSkill(message.content[1:])
    await message.channel.send(message.author.mention +"\n" +'**Name:** '+name+"\n"+'**Desc:** '+desc+"\n"+'**Ability Mod:** '+abi)

  if re.fullmatch(prefix+r'damage',message.content):
    damage = damageList()
    await message.channel.send(message.author.mention +"\n" +'**Damage Types:** '+damage)
  
  if re.fullmatch(r'&acid|&bludgeoning|&cold|&fire|&force|&lightning|&necrotic|&piercing|&poison|&psychic|&radiant|&slashing|&thunder',message.content):
    (name,desc)=searchDamage(message.content[1:])
    await message.channel.send(message.author.mention +"\n" +'**Damage Type:** '+name+"\n"+'**Desc:** '+desc)

  if re.fullmatch(prefix+r'help',message.content):
    await message.channel.send(message.author.mention +"\n" + helpList())

keep_alive()
client.run(os.getenv('TOKEN'))
