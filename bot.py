import os
import random
import discord
import re
import io
from PIL import Image, ImageDraw
import requests

client = discord.Client()

hotwords = [
    re.compile('\\btit\\b'),
    re.compile('\\btits\\b'),
    re.compile('\\btitty\\b'),
    re.compile('\\btitties\\b')
]

wth = [
    re.compile('\\bwhat in the (god damn|goddamn) hell are you talkin\'?g? bout\\b\?'),
    re.compile('\\bwhat are you talking? about\\b\??'),
    re.compile('\\b(what the (hell|fuck)|wt(h|f)) are you talking? about\\b\??')
]

froyo_captions = [
    "You're in Gerald's world now baby!",
    "It was *cold*, but it wasn't ***frozen***!",
    "Why do you ***LIE*** to me??"
]


def discrete_phrase(phrase):
    return re.compile('\\b' + phrase + '\\b')


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(msg):
    if msg.author.id == client.user.id: return

    if any(re.search(regex, msg.content.lower()) for regex in hotwords):
        await client.send_file(msg.channel, 'thetits.png')

    if re.search(discrete_phrase('what if it was purple'), msg.content.lower()):
        attachment = None

        try:
            attachment = msg.attachments[0]['url']
        except IndexError:
            try:
                last_msg = await get_logs_from_channel(msg.channel)
                attachment = last_msg.attachments[0]['url']
            except IndexError:
                await client.send_message(msg.channel, 'Nothing to make purple!')

        if attachment is not None:
            try:
                img = Image.open(io.BytesIO(requests.get(attachment).content)).convert('RGBA')
                tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(tmp)
                draw.rectangle((0, 0) + img.size, fill=(85, 26, 139, 175))

                img = Image.alpha_composite(img, tmp)
                imgbytearr = io.BytesIO()
                img.save(imgbytearr, format='PNG')
                imgbytearr = imgbytearr.getvalue()
                await client.send_file(msg.channel, io.BytesIO(imgbytearr), filename='its-purple.png')
            except OSError:
                await client.send_message(msg.channel, 'Looks like the last sent file isn\'t an image!')

    if re.search(discrete_phrase('wack'), msg.content.lower()):
        await client.send_file(msg.channel, 'wack.png')

    if re.search(discrete_phrase('boo'), msg.content.lower()):
        await client.send_file(msg.channel, 'imright.png')

    if re.search(discrete_phrase('bird up'), msg.content.lower()):
        await client.send_file(msg.channel, 'birdup.jpg')

    if re.search(discrete_phrase('rice'), msg.content.lower()):
        await client.send_file(msg.channel, 'rice.png')

    if re.search('\\bhannibal (bustin\'?|busting) (thru|through)\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'hbt.jpg')

    if re.search(discrete_phrase('call me'), msg.content.lower()):
        await client.send_file(msg.channel, 'callme.jpg')

    if re.search('(brb|be right back)', msg.content.lower()):
        await client.send_file(msg.channel, './brb/' + random.choice(os.listdir('./brb')))

    if re.search(discrete_phrase('who killed hannibal?'), msg.content.lower()):
        await client.send_file(msg.channel, 'death.png')

    if re.search('\\bburgers?\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'burgers.gif')

    if re.search('\\b(get yourself together|move to (philly|philadelphia)|philly|philadelphia|hummus)\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'philly.jpg')

    if re.search(discrete_phrase('why would you say something so controversial yet so brave?'), msg.content.lower()):
        await client.send_file(msg.channel, 'sobrave.gif')

    if any(re.search(regex, msg.content.lower()) for regex in wth):
        await client.send_file(msg.channel, 'wth.gif')

    if re.search(discrete_phrase('bitch'), msg.content.lower()):
        await client.send_file(msg.channel, 'bitch.png')

    if re.search(discrete_phrase('i\'m dying'), msg.content.lower()):
        await client.send_file(msg.channel, 'dying.jpg')

    if re.search(discrete_phrase('catch the excitement'), msg.content.lower()):
        await client.send_file(msg.channel, 'excitement.png')

    if re.search(discrete_phrase('beer'), msg.content.lower()):
        await client.send_file(msg.channel, 'morpheus.png')

    if re.search(discrete_phrase('weed'), msg.content.lower()):
        await client.send_file(msg.channel, '520bro.jpg')

    if re.search('\\bfrozen (yogurt|yoghurt)\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'froyo.png', content=random.choice(froyo_captions))

    if re.search('(investigate (311|3/11)|\\b(311|3/11)\\b)', msg.content.lower()):
        await client.send_file(msg.channel, '311.png')

    if re.search('\\b(dinosaur|dino|stegosaurus|safety stegosaurus|safety dinosaur)\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'dinosaur.png')

    if re.search('\\b(froot loops|fruit loops)\\b', msg.content.lower()):
        await client.send_file(msg.channel, 'frootloops.png')

    if re.search('\\bquestlove\\b', msg.content.lower()):
        if re.search("\\bquestlove you're not in the house\\b", msg.content.lower()):
            await client.send_file(msg.channel, 'notinthehouse.png', content="Questlove you're not in the house. You're nowhere...")
        else:
            await client.send_file(msg.channel, 'questlove.png', content="Yo " + msg.author.mention + "... Questlove's in the house!")

async def get_logs_from_channel(channel):
    async for m in client.logs_from(channel):
        if m.attachments:
            try:
                i = Image.open(io.BytesIO(requests.get(m.attachments[0]['url']).content)).convert('RGBA')
                return m
            except OSError:
                # Not an image attachment
                continue

    return None


async def get_last_message_from(channel, message):
    async for m in client.logs_from(channel, limit=1, before=message):
        return m

client.run(os.environ["bot_token"])
