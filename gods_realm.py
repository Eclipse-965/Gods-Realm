# -*- coding: utf-8 -*-
"""
Created on Sun May 12 14:21:42 2024
@author: Eclipse-965
"""
import random
import time
import json
import traceback

inventory = []
entered=''
location = 'clearing'
locations = {
    'clearing': {
        'items': ['stick'],
        'north': 'crossroads_north',
        'south': 'beach',
        'west':'gate',
        'east': 'forest_eye',
        'monsters': [],
        'objects':[],
        'blocks': {
            'west':'placeholder_barrier',
            'placeholder_barrier':'west'},
        'description': 'A forest clearing with paths leading off in all 4 directions.',
        'display':'A clearing'
    },
    'forest_eye': {
        'items': [],
        'west': 'clearing',
        'east':'clearing_sword',
        'monsters': ['eyebat'],
        'objects':[],
        'blocks':{},
        'end_description':'A path running east-west through the forest.',
        'description': 'A path running east-west through the forest, blocked by a giant eyeball with jet-black, leathery wings.\nA sword gleams in a clearing to the east.',
        'display':'A forest path.'
    },
    'clearing_sword': {
        'items': ['iron sword'],
        'objects':[],
        'west':'forest_eye',
        'description':'A clearing in the forest with a singular path leading off to the west.',
        'display':'A clearing.',
        'blocks':{},
        'monsters':[]
    },
    'gate': {
        'items':[],
        'monsters': ['talos'],
        'description':'A large bronze gate, guarded by a giant automaton',
        'display':'A gate',
        'east':'clearing',
        'blocks':{
            'bronze gate':'west',
            'west':'bronze gate'},
        'west':'',
        'objects':['bronze gate']
        },
    'crossroads_north': {
        'items':[],
        'monsters':[],
        'description':'A crossroads in the forest, paths leading off to the north, south, and east.',
        'display':'A crossroads',
        'blocks':{},
        'east':'enchanted_clearing',
        'north':'',
        'south':'clearing',
        'objects':[]
        },
    'beach': {
        'items':[],
        'monsters':[],
        'description':'A sandy beach. A path lies to the east.',
        'display':'A beach',
        'north':'clearing',
        'east':'crab_shrine',
        'south':'',
        'objects':[],
        'blocks':{
            'south':'coast',
            'coast':'south'}
        },
    'crab_shrine': {
        'items':[],
        'monsters':['giant crab'],
        'description':'A shrine built around a crab statue.',
        'display':'A crab shrine',
        'west':'beach',
        'objects':['crab statue'],
        'blocks':{}
        },
    'enchanted_clearing': {
        'items':[],
        'monsters':['dryad'],
        'description':'A large clearing in the woods with a mystical air to it, along with a large oak tree in the centre. An angry dryad steps out of the tree, ready to fight.',
        'display':'A mystical clearing',
        'west':'crossroads_north',
        'objects':[],
        'blocks':{},
        'end_description':'A large clearing in the woods with a mystical air to it, with a large oak tree standing in the centre. A singular path leads off to the west.',
        },
    '': {
        'items':[],
        'monsters':[],
        'description':"You aren't supposed to be here.",
        'display':"forbidden area",
        'objects':[],
        'blocks':{}}
    }


monsters = {
    'eyebat': {
        'health': 10,
        'armour': 1,
        'deathmessage':'The eyebat shrivels up on the ground and vanishes in a cloud of black dust.',
        'display':'an eyebat',
        'drops':['eyebat wing membrane'],
        'escapechance':2,
        'expgain':10,
        'bonuses': {
            'piercing': 1.9
        },
        'attacks': {
            'charges at you': {
                'lowdamage': 2,
                'highdamage': 5,
                'type': 'blunt'
            },
            'flaps its wings forcefully at you':{
                'lowdamage':3,
                'highdamage':7,
                'type':'wind'}
        }
    },
    'talos': {
        'health':30,
        'armour':0.8,
        'deathmessage':'The automaton turns to rust and disintegrates',
        'display':'A giant bronze automaton',
        'escapechance':5,
        'drops':['bronze gate key'],
        'bonuses':{
            'water':1.15,
            'piercing':1.2,
            'slashing':0.78,
            'blunt':0.62,
            'fire':0.58},
        'attacks':{
            'steps on you':{
                'lowdamage':8,
                'highdamage':13,
                'type':'blunt'},
            'swipes at you with his hand':{
                'lowdamage':8,
                'highdamage':12,
                'type':'blunt'},
            'belches fire at you': {
                'lowdamage':10,
                'highdamage':14,
                'type':'fire'}}
        },
    'giant crab': {
        'health':20,
        'armour':0.75,
        'highexpgain':20,
        'lowexpgain':16,
        'deathmessage':'The giant crab tips over and curls up before disintegrating.',
        'escapechance':3,
        'bonuses': {
            'water':0.5,
            'fire':1.13,
            'piercing':1.2,
            'slashing':0.888},
        'attacks': {
            'squeezes you between its pincers': {
                'lowdamage':5,
                'highdamage':8,
                'type':'blunt'},
            'shoots a beam of water at you':{
                'lowdamage':3,
                'highdamage':7,
                'type':'water'},
            'jabs you with its claw': {
                'lowdamage':6,
                'highdamage':9,
                'type':'piercing'}
            },
        'drops':['conch shell']
        },
    'dryad': {
        'health':17,
        'armour':1,
        'drops':['soul of dryad'],
        'deathmessage':'The dryad falls to the ground and fades away, leaving its soul behind.',
        'expgain':15,
        'escapechance':3,
        'bonuses':{
            'nature':0.4,
            'water':0.8,
            'fire':1.3},
        'attacks': {
            'traps you with vines': {
                'lowdamage':6,
                'highdamage':9,
                'type':'nature'},
            'saps your life energy': {
                'lowdamage':2,
                'highdamage':5,
                'type':'necrotic'}}
        },
}
objects = {
    'bronze gate':
        {'type':'locked_door',
         'key':'bronze gate key',
         'description':'A large bronze gate',
         'error':'A bronze gate blocks the path.',
         'interact':'You put the key in the lock and the gate swings open, revealing the path the Colchis.'
         },
    'placeholder_barrier':
        {'type':'locked_door',
         'key':'debug_weapon',
         'description':'this area is off limits for now',
         'error':"You can't go that way yet",
         'interact':'You got past the placeholder barrier (somehow)'},
    'crab statue':
        {'type':'locked_chest',
         'key':'conch shell',
         'description':'A large crab statue with a small hole in the shell, just large enough to fit a conch shell inside.',
         'interact':"You put the conch into the shell of the crab statue. It opens up like a treasure chest.",
         'items':['crab armour'],
         'space':3
         },
    'coast': {
        'type':'environment_barrier',
        'key':'crab armour',
        'description':'A line of impenetrable waves',
        'keytype':'armour'}}
    
items = {
    'stick': {
        'type': 'weapon',
        'tags':['usable'],
        'description': 'A very pointy stick',
        'attacks': {
            'poke': {
                'lowdamage': 1,
                'highdamage': 3,
                'type': 'piercing'
            }
        }
    },
    'plate armour': {
        'type': 'armour',
        'protection': 0.8,
        'tags':['usable'],
        'description': 'Simple plate armour.',
        'bonuses': {
            'slashing': 0.76,
            'blunt': 0.8,
            'piercing': 1.25,
            'wind':0.6
        },
        
    },
    'iron sword': {
        'type': 'weapon',
        'description':'A shiny iron sword',
        'tags':['usable'],
        'attacks':{
            'jab':{
                'lowdamage':4,
                'highdamage':8,
                'type':'piercing'},
            'slash':{
                'lowdamage':4,
                'highdamage':9,
                'type':'slashing'},
            'pommel strike':{
                'lowdamage':2,
                'highdamage':5,
                'type':'blunt'}}
    },
    'bronze gate key': {
        'type':'key',
        'description':'A simple key made of Bronze.'
        },
    'debug_weapon': {
        'type':'weapon',
        'description':'The power of weezer in your hands',
        'tags':['usable'],
        'attacks':{
            'kill':{
                'lowdamage':999999999,
                'highdamage':1000000000,
                'type':'debug'}}
        },
    'debug_armour': {
        'type':'armour',
        'description':'Weezersuit',
        'tags':['usable'],
        'protection':0,
        'bonuses':{
            'debug':0}
        },
    'crab armour': {
        'type':'armour',
        'description':'A crablike suit of armour',
        'tags':['usable'],
        'protection':0.75,
        'bonuses':{
            'water':0.5,
            'fire':1.13,
            'piercing':1.2,
            'slashing':0.888}
        },
    'conch shell': {
        'type':'key',
        'description':'A small conch shell.'
        },
    'soul of dryad': {
        'type':'heal_potion',
        'description':'A glowing green orb',
        'heal_value':8,
        'use':"You absorb the dryad's soul, replenishing your health.",
        'uses':1,
        'tags':['usable']
        },
    'eyebat wing membrane': {
        'type':'material',
        'description':'A tough, leathery membrane.'
        }
}

debug=False
health=0
weapon = ''
armour = ''
player = {'max_health': 15,
          'health': 15,
          'level':1,
          'exp_req':10,
          'exp':0}  

def kill(monster):
    locations[location]['monsters'].remove(monster)
    try:
        locations[location]['description']=locations[location]['end_description']
    except KeyError:
        pass
    for item in monsters[monster]['drops']:
        locations[location]['items'].append(item)
    print(monsters[monster]['deathmessage'])
    time.sleep(1)
    if monsters[monster]['drops']:
        print('It dropped:',', '.join(monsters[monster]['drops']))
    level_up(monster)

def inspect(item):
    if item not in inventory and item!=armour and item != weapon:
        print("You aren't carrying that item.")
        return
    print(item,'-',items[item]['description'])
    type=items[item]['type']
    if 'potion' in type:
        print(f"Remaining uses - {items[item]['uses']}")
        if type=='heal_potion':
            print(f"Healing power - {items[item]['heal_value']}")

def use(item):
    global inventory
    global items
    if item not in inventory:
        print("You don't have that item in your inventory.")
        return
    type=items[item]['type']
    if type=='armour' or type=='weapon':
        print('Try equipping this item instead!')
    elif type=='heal_potion':
        print(items[item]['use'])
        player['health']+=items[item]['heal_value']
        if player['health']>player['max_health']:
            player['health']=player['max_health']
    else:
        print("I don't know what to put here, but you can't use that thing.")
    if 'potion' in type:
        items[item]['uses']-=1
        if items[item]['uses']<=0:
            print('You exhausted the uses of the item.')
            inventory.remove(item)
    

def save_game(filename):
    if filename[-5:]!='.json':
        filename+='.json'
    game_state= {
        'inventory':inventory,
        'location':location,
        'weapon':weapon,
        'armour':armour,
        'player':player,
        'entered':entered,
        'debug':debug,
        'location_data':locations,
        'item_data':items,
        'object_data':objects
        }
    with open(filename, 'w') as file:
        json.dump(game_state,file)
        print('Game saved as',filename+'.')

def level_up(monster):
    global player
    print(f"\nYou got {monsters[monster]['expgain']} exp!")
    try:
        player['exp']+=random.randrange(monsters[monster]['lowexpgain'],monsters[monster]['highexpgain'])
    except KeyError:
        player['exp']+=monsters[monster]['expgain']
    newlevel=player['level']
    while player['exp_req']<=player['exp']:
        newlevel=player['level']+1
        player['exp']-=player['exp_req']
        player['exp_req']=int(round(player['exp_req']*1.15,0))
        player['max_health']*=1.2
        player['health']=int(player['max_health'])
    if newlevel!=player['level']:
        print(f'You are now level {newlevel}!')
        player['level']=newlevel

def load_game(filename):
    global inventory, location, weapon, armour, player, entered, debug, locations, items, objects
    if filename[-5:]!='.json':
        filename+='.json'
    try:
        with open(filename,'r') as file:
            game_state=json.load(file)
            inventory=game_state['inventory']
            location=game_state['location']
            weapon=game_state['weapon']
            armour=game_state['armour']
            player=game_state['player']
            entered=game_state['entered']
            debug=game_state['debug']
            locations=game_state['location_data']
            items=game_state['item_data']
            objects=game_state['object_data']
        print(filename,'successfully loaded.')
        stats()
    except FileNotFoundError:
        print('No saved game found.')

def open_locked_chest(item):
    if objects[item]['key'] in inventory:
        print(objects[item]['interact'])
        inventory.remove(objects[item]['key'])
        objects[item]['type']='chest'
        open_chest(item)
    else:
        print("You aren't carrying the correct key.")
        
def open_chest(item):
    if objects[item]['items']:
        print("Inside the chest, there lies:",', '.join(objects[item]['items']))
    else:
        print("The chest is empty.")
    removal=input('\nWhat would you like to do with the chest? (take/drop/leave)\n').lower().split()
    while removal:
        try:
            object=' '.join(removal[1:])
            if removal[0]=='take':
                if object in objects[item]['items'] and len(inventory)<=10:
                    print(f"You got {object}!")
                    objects[item]['items'].remove(object)
                    inventory.append(object)
                elif object not in objects[item]['items']:
                    print("That item isn't in the chest.")
                else:
                    print('Your inventory is full!')
            elif removal[0]=='drop':
                if object in inventory:
                    print(f"You left {object} in the chest!")
                    objects[item]['items'].append(object)
                    inventory.remove(object)
                else:
                    print("You don't have that in your inventory.")
            elif removal[0]=='leave':
                print('You left the chest.')
                return            
        except IndexError:
            print("You left the chest.")
            return
        removal=input('\nWhat would you like to do with the chest?\n').lower().split()
            
def interact(item):
    if item in objects:
        if objects[item]['type']=='locked_door':
            if objects[item]['key'] in inventory:
                print(objects[item]['interact'])
                inventory.remove(objects[item]['key'])
                del locations[location]['blocks'][locations[location]['blocks'][item]]
                del locations[location]['blocks'][item]
        elif objects[item]['type']=='locked_chest':
            open_locked_chest(item)
        elif objects[item]['type']=='chest':
            open_chest(item)
    else:
        print("That object isn't here!")
                
def look():
    displays=[]
    print(locations[location]['description'])
    if len (locations[location]['monsters'])>=1:
        for monster in locations[location]['monsters']:
            displays.append(monsters[monster]['display'])
            print(str(' '.join(displays)).capitalize())
    if locations[location]['items']:
        print("There lies", ', '.join(locations[location]['items'])+'.')
    if locations[location]['objects']:
        print("There is a", ', '.join(locations[location]['objects'])+'.')

def equip(item):
    global weapon
    global armour
    if item in inventory:
        type=items[item]['type']
        if type=='weapon' or type=='armour':
            print(item, 'was equipped!')
        else:
            print("You can't equip that item.")
        if type == 'weapon':
            if weapon != '':
                inventory.append(weapon)
            weapon = item
        elif type == 'armour':
            if armour != '':
                inventory.append(armour)
            armour = item
        inventory.remove(item)
    else:
        print("You don't have that item.")

def putdown(location, item):
    if item in inventory:
        inventory.remove(item)
        locations[location]['items'].append(item)
        print('You left', item, 'in', locations[location]['display'] + '.')
    else:
        print((item), 'is not in your inventory.')

def pickup(item):
    if item in locations[location]['items']:
        if len(inventory) <=10:
            inventory.append(item)
            locations[location]['items'].remove(item)
            print(f'You got {item}!')
        else:
            print('Your inventory is full.')
    else:
        print(item, 'is not available here.')

def gosuccess(direction):
    global location
    global entered
    location=locations[location][direction]
    print(locations[location]['description'])
    if direction=='west':
        entered='east'
    elif direction=='south':
        entered='north'
    elif direction=='east':
        entered='west'
    elif direction=='north':
        entered='south'
    if len(locations[location]['items']) >= 1:
        print("There lies", ', '.join(locations[location]['items'])+'.')
    if location=='':
        print('You were moved to the clearing.')
        location='clearing'

def go(direction):
    

    global entered
    global location
    if direction in locations[location]:
        if direction not in locations[location]['blocks'] and len(locations[location]['monsters'])==0:
            gosuccess(direction)
        elif len(locations[location]['monsters'])!=0:
            if direction!=entered:
                print('A monster blocks your path!')
            else:
                gosuccess(direction)
        elif objects[locations[location]['blocks'][direction]]['type']=='locked_door':
            print(objects[locations[location]['blocks'][direction]]['error'])
        elif objects[locations[location]['blocks'][direction]['type']]=='environment_barrier':
            if objects[locations[location]['blocks'][direction]]['keytype']=='armour':
                if objects[locations[location]['blocks'][direction]]['key']==armour:
                    gosuccess(direction)
                elif objects[locations[location]['blocks'][direction]]['key'] in inventory:
                    print('Try equipping your',objects[locations[location]['blocks'][direction]]['key']+'!')
                else:
                    print('Something is blocking your path to the',direction+'!')
            elif objects[locations[location]['blocks'][direction]]['keytype']=='weapon':
                if objects[locations[location]['blocks'][direction]]['key']==armour:
                    gosuccess(direction)
                elif objects[locations[location]['blocks'][direction]]['key'] in inventory:
                    print('Try equipping your',objects[locations[location]['blocks'][direction]]['key']+'!')
                else:
                    print('Something is blocking access to the',direction+'!')
            elif objects[locations[location]['blocks'][direction]]['keytype']=='inventory':
                if objects[locations[location]['blocks'][direction]]['key'] in inventory:
                    gosuccess(direction)
                else:
                    print('Something is blocking access to the',direction+'!')
    else:
        print('You cannot go that way.')

def attack(attack,monster):
    global health
    print('You', attack, 'the', monster + '.')
    damage = random.randrange(items[weapon]['attacks'][attack]['lowdamage'], items[weapon]['attacks'][attack]['highdamage'])
    if items[weapon]['attacks'][attack]['type'] in monsters[monster]['bonuses']:
        damage = int(round(damage * monsters[monster]['armour']*monsters[monster]['bonuses'][items[weapon]['attacks'][attack]['type']], 0))
    else:
        damage=int(round(damage*monsters[monster]['armour'],0))
    print('It dealt', damage, 'damage!')
    if items[weapon]['attacks'][attack]['type']=='necrotic':
        print("You regained {int(round(damage/2.4),0)} health!")
        player['health']+=int(round(damage/2.4),0)
    health -= damage
    if health <= 0:
        kill(monster)
        return('dead')
    else:
        print(f'The {monster} was knocked down to {health} health.\n')

def playerturn(monster):
    global player, health
    set=input("What do you want to do? (attack/flee/item)\n").lower()
    while set!='attack' and set!='flee' and set!='item':
        print("That is not a valid response.")
        set=input("What do you want to do? (attack/flee/item)\n").lower()
    if set=='attack':
        print('Possible attacks:', '/'.join(items[weapon]['attacks']))
        yourattack = input("Which attack would you like to use?\n").lower()
        while yourattack not in items[weapon]['attacks']:
            print("You can't use that attack with this weapon!")
            yourattack = input("Which attack would you like to use?\n").lower()
        if attack(yourattack,monster)=='dead':
            return('dead')
    elif set=='flee':
        escaped=random.randrange(monsters[monster]['escapechance'])
        if escaped==1:
            print('You escaped!')
            return('escaped')
        else:
            print("You didn't get away.")
            return
    elif set=='item':
         if use_fight()==False:
             return(False)
        
def use_fight():
    usable=[]
    for item in inventory:
        try:
            if 'usable' in items[item]['tags']:
                usable.append(item)
        except KeyError:
            pass
    if usable:
        print("Usable items:",', '.join(usable))
        item=input("\nWhich item would you like to use?\n")
        while item not in usable:
            print("You can't use that item!")
            item=input("\nWhich item would you like to use?\n")
        if 'potion' in items[item]['type']:
            use(item)
            return(True)
        else:
            equip(item)
            return(False)
    else:
        print("You don't have any items that you can use in combat.")
        return(False)
    
    
def monsterturn(monster):
    global player, health
    attack = random.choice(list(monsters[monster]['attacks'].keys()))
    damage = random.randrange(monsters[monster]['attacks'][attack]['lowdamage'], monsters[monster]['attacks'][attack]['highdamage'])
    if armour != '':
        if monsters[monster]['attacks'][attack]['type'] in items[armour]['bonuses']:
            damage = int(round(damage * items[armour]['bonuses'][monsters[monster]['attacks'][attack]['type']], 0))
    print(f"The {monster} {attack}!")
    print(f"It dealt {damage} damage!")
    if monsters[monster]['attacks'][attack]['type']=='necrotic':
        health+=int(round(damage/2.4))
        print(f"The monster regained {int(round(damage/2.4))} health!")
    player['health']-=damage
    if player['health'] > 0:
        print(f"You have {player['health']} health remaining.\n")
    else:
        print('You died.')
        return('dead')

def fight():
    global player, health
    if weapon=='':
        print("You don't have a weapon equipped!")
        return()
    if locations[location]['monsters']:
        monster=input("Which monster would you like to fight?\nMonsters: "+'/'.join(locations[location]['monsters'])+'\n')
        while monster not in locations[location]['monsters']:
            print("That monster doesn't exist here!")
            monster=input("Which monster would you like to fight?\nMonsters: "+'/'.join(locations[location]['monsters'])+'\n')
        health = monsters[monster]['health']
        while health > 0 and player['health'] > 0:
            result=playerturn(monster)
            while result==False:
                result=playerturn(monster)
            if result=='dead' or result=='escaped':
                return
            time.sleep(1)
            if monsterturn(monster)=='dead':
                return('dead')
            time.sleep(1)
            
    else:
        print('There are no monsters here.')

def stats():
    print(f"Health - {player['health']}")
    if armour!='':
        print(f"Armour - {armour}")
    else:
        print('Armour - none')
    if weapon!='':
        print(f"Weapon - {weapon}")
    else:
        print('Weapon - none')
    print('Location -',locations[location]['display'])
    print(f"Level - {player['level']}")
    print(f"Exp - {player['exp']}")

def game_intro():
    print('You wake up in a forest clearing, paths leading off in all 4 directions.')
    print('A large stick dwells in the centre of the clearing.')

def main():
    game_intro()
    while True:
        global weapon
        global debug
        global armour
        global location
        global command
        command = input('\nWhat would you like to do?\n')    .split()
        if command[0] == 'drop':
            putdown(location, ' '.join(command[1:]))
        elif command[0] == 'quit':
            print("Thank you for playing Gods' Realm.")
            time.sleep(5)
            break
        elif command[0] == 'take':
            pickup(' '.join(command[1:]))
        elif command[0] == 'go':
            go(command[1])
        elif command[0] == 'help':
            print("""
            Commands:
            go [direction] - Moves in a specified direction.
            take [item] - Move an item into your inventory.
            inventory - Checks the contents of your inventory.
            drop [item] - Removes a specified item from your inventory.
            help - Gives a list of commands
            equip [item] - Equips a specified item from your inventory.
            fight - enter combat with a monster.
            stats - Checks your stats.
            look - Shows what's around you.
            interact [object] - Interact with a specified object.
            save [filename] - saves your file as a json.
            load [filename] - loads a specified save file.
            use [item] - uses a specified item from your inventory.
            inspect [item] - shows you some information on a specified item in your inventory.
            """)
        elif command[0] == 'inventory':
            if len(inventory) > 0:
                print('Inventory:', ' '.join(inventory))
            else:
                print('Your inventory is empty.')
        elif command[0] == 'equip':
            equip(' '.join(command[1:]))
        elif command[0] == 'fight':
            if inventory!='':
                if fight()=='dead':
                    print("Thank you for playing Gods' Realm.")
                    time.sleep(2)
                    if input('Press enter to quit game.')=='':
                        return
            else:
                print('You need to have a weapon equipped!')
        elif command[0]=='stats':
            stats()
        elif command[0]=='look':
            look()
        elif command[0]=='interact':
            interact(' '.join(command[1:]))
        elif ' '.join(command)=='lemon on the chain with the v-cut (yeah)':
            if debug==False:
                print('Debug mode on')
                weapon='debug_weapon'
                armour='debug_armour'
                debug=True
                print("""
                      New command:
                          Teleport [location] - teleport to a location.
                      """)
            else:
                print('Debug mode off')
                debug=False
        elif command[0]=='teleport':
            if debug==True:
                if (' '.join(command[1:])) in locations:
                    location = (' '.join(command[1:]))
                    print("Welcome to",location+'!')
        elif command[0]=='save':
            save_game((' '.join(command[1:])))
        elif command[0]=='load':
            load_game((' '.join(command[1:])))
        elif command[0]=='use':
            use((' '.join(command[1:])))
        elif command[0]=='inspect':
            inspect((' '.join(command[1:])))
        else:
            print("Unknown command or missing argument. Type 'help' for command list.")
try:       
    main()
except Exception:
    traceback.print_exc()
    print()
    print("Please record the error and upload it to the 'bugs' topic of the community tab on itch!")
    print("Press enter to close the game after recording.")
    input('')

