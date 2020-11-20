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

if len(sys.argv) == 2:
    print(sys.argv[1])

logging.basicConfig(level=logging.INFO)
with open('login.txt', 'rt') as f,\
     open('./teams/test1.txt', 'rt') as team:
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
            await room_obj.say('Oh my, look at the time! Gotta go, gg.')
            await room_obj.forfeit()
            await room_obj.leave()


    async def on_poke(self, params):
        print("Poke: " + str(params))

ChallengeClient(name=username, password=password).start()
