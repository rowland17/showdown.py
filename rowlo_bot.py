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
from pprint import pprint



p1_team = []
p2_team = []


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
        if room_obj.id.startswith('battle-'):
            await asyncio.sleep(3)
#            await room_obj.say('Oh my, look at the time! Gotta go, gg.')
#            await room_obj.forfeit()
#            await room_obj.leave()
            p1_team = []
            p2_team = []


    async def on_poke(self, params):
        print(params[0])
        if params[0] == 'p1':
            p1_team.append(params[1].split(',')[0])
            print(p1_team)
        else:
            p2_team.append(params[1].split(',')[0])
            print(p2_team)


    async def on_teampreview(self, params):
        print("hello")


    async def on_turn(self, room_obj, params):
        await room_obj.switch('3')


    async def on_faint(self, room_obj, params):
        await room_obj.switch('3')

    async def on_receive(self, room_id, inp_type, params):
        print("Input type: " + str(inp_type) + " Params: " + str(params))

ChallengeClient(name=username, password=password).start()
