import os
import random
import re

import discord

client = discord.Client()

froyo_captions = [
    "You're in Gerald's world now baby!",
    "It was *cold*, but it wasn't ***frozen!***",
    "Why do you ***LIE*** to me??"
]


def message_has_trigger(msg, keyword):
    return re.search('\\b' + keyword + '\\b', msg.content.lower())


async def send_image(channel, img, caption=''):
    await client.send_file(channel, './img/' + img, content=caption)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(msg):
    if msg.author.id == client.user.id:
        return

    elif message_has_trigger(msg, '(investigate (311|3/11)|(311|3/11))'):
        await send_image(msg.channel, '311.png')

    elif message_has_trigger(msg, 'weed'):
        await send_image(msg.channel, '520bro.jpg')

    elif message_has_trigger(msg, 'christina applegate'):
        await send_image(msg.channel, 'applegate.png', caption='Quick shoutout to Christina Applegate!')

    elif message_has_trigger(msg, 'grizzly bear'):
        await send_image(msg.channel, 'bear.png')

    elif message_has_trigger(msg, 'bird up'):
        await send_image(msg.channel, 'birdup.jpg')

    elif message_has_trigger(msg, 'bitch'):
        await send_image(msg.channel, 'bitch.png')

    elif message_has_trigger(msg, '(burger|hamburger|cheeseburger)s?'):
        await send_image(msg.channel, 'burgers.gif')

    elif message_has_trigger(msg, 'call me'):
        await send_image(msg.channel, 'callme.jpg')

    elif message_has_trigger(msg, 'coachella'):
        await send_image(msg.channel, 'coachella.png')

    elif message_has_trigger(msg, 'who killed hannibal\\??'):
        await send_image(msg.channel, 'death.png')

    elif message_has_trigger(msg, '(dinosaur|dino|stegosaurus|safety stegosaurus|safety dinosaur)'):
        await send_image(msg.channel, 'dinosaur.png')

    elif message_has_trigger(msg, '(catch the excitement|excited)'):
        await send_image(msg.channel, 'excitement.png')

    elif message_has_trigger(msg, '(froot|fruit) loops'):
        await send_image(msg.channel, 'frootloops.png')

    elif message_has_trigger(msg, '(frozen (yogurt|yoghurt)|froyo)'):
        await send_image(msg.channel, 'froyo.png', caption=random.choice(froyo_captions))

    elif message_has_trigger(msg, 'hannibal (bustin\'?|busting) (thru|through)'):
        await send_image(msg.channel, 'hbt.jpg')


client.run(os.environ["bot_token"])
