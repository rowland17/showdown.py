# -*- coding: utf-8 -*-
"""
An example client that challenges a player to 
a random battle when PM'd, or accepts any
random battle challenge.
"""
import showdown
import sys
import logging
import asyncio
import random

from pprint import pprint
from pokemon import *


global NO_TARGET_MOVES
NO_TARGET_MOVES = [
    "protect",
    "outrage",
    "electroweb",
    "rockslide"
]


global myTeam
myTeam = True
global p1_team
global p2_team
print ("test")
p1_team = []
p2_team = []
global poke_on_field


if len(sys.argv) == 2:
    battle_team = sys.argv[1]
else:
    battle_team = "./teams/test1.txt"

logging.basicConfig(level=logging.INFO)
with open('login.txt', 'rt') as f,\
     open(battle_team, 'rt') as team:
    username, password = f.read().strip().splitlines()
    vgc_team = team.read()

class ChallengeClient(showdown.Client):
    async def on_private_message(self, pm):
        if pm.recipient == self:
            await self.cancel_challenge()
            await pm.author.challenge('', 'gen8randombattle')

    async def on_challenge_update(self, challenge_data):
        incoming = challenge_data.get('challengesFrom', {})
        for user, tier in incoming.items():
            if 'random' in tier:
                await self.accept_challenge(user, 'null')
            elif 'gen7monotype' in tier:
                await self.accept_challenge(user, vgc_team)
            elif 'gen8vgc2021' in tier:
                print("Hey scott")
                await self.accept_challenge(user, vgc_team)
            else:
                print(tier)
                

    async def on_room_init(self, room_obj):
        global p1_team
        global p2_team
        global poke_on_field
        if room_obj.id.startswith('battle-'):
#            await room_obj.say('Oh my, look at the time! Gotta go, gg.')
#            await room_obj.forfeit()
#            await room_obj.leave()
            p1_team = []
            p2_team = []
            poke_on_field = []

    
    async def on_player(self, params):
        global myTeam
        if params[0] == 'p1' and params[1] == username:
            print("myTeam is true")
            myTeam = True
        else:
            print("myTeam is false")
            myTeam = False

    async def on_poke(self, params):
        global p1_team
        global p2_team
        print(params[0])
        if params[0] == 'p1':
            p1_team.append(Pokemon(params[1].split(',')[0]))
            print(p1_team)
        else:
            p2_team.append(Pokemon(params[1].split(',')[0]))
            print(p2_team)


    async def on_teampreview(self, room_obj, params):
        global myTeam
        global p1_team
        global p2_team
        if myTeam:
            poke_on_field.append(2) #to match 2134 below...
            poke_on_field.append(1)
        else:
            poke_on_field.append(2) #to match 2134 below...
            poke_on_field.append(1)
        await room_obj.start_poke("2134")
        

    #TODO attack_switch, switch_attack, double_attack


    #TODO make more sensible switches. 
    async def on_turn(self, room_obj, params):
        global myTeam
        global p1_team
        global p2_team
        print("p1_team_empty")
        print(p1_team)
        #rand = random.randint(0, 1)
        rand = 1
        if rand == 0:
            if myTeam:
                await room_obj.double_switch(p1_team[2].name, p1_team[3].name)
            else:
                await room_obj.double_switch(p2_team[3].name, p2_team[2].name)
        elif rand == 1:
            if myTeam:
                await room_obj.double_attack(p1_team[poke_on_field[0]-1].moves[2], '1', p1_team[poke_on_field[1]-1].moves[2], '1')
            else:
                await room_obj.double_attack(p2_team[poke_on_field[0]-1].moves[2], '1', p2_team[poke_on_field[1]-1].moves[2], '1')
        else:
            print("BAD RAND NUMBER - TURN")
        


    #TODO make more sensible switches. 
    async def on_faint(self, room_obj, params):
        global myTeam
        global p1_team
        global p2_team
        player, mon = params[0].split(": ")

        if 'p1' in player:
            #remove from our team
            for poke in p1_team:
                if mon == poke.name:
                    p1_team.remove(poke)
                    break
        else:
            #remove from team 2
            for poke in p2_team:
                if mon == poke.name:
                    p2_team.remove(poke)
                    break
        
        if myTeam:
            await room_obj.switch('3')
        else:
            await room_obj.switch('3')


    async def on_receive(self, room_id, inp_type, params):
        print("Input type: " + str(inp_type) + " Params: " + str(params))

ChallengeClient(name=username, password=password).start()
