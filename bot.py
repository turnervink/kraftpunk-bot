import os
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

# TODO: use regex to not match words in words

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(msg):
    if any(re.search(regex, msg.content.lower()) for regex in hotwords):
        await client.send_file(msg.channel, 'thetits.png')

    if 'what if it was purple' in msg.content.lower():
        try:
            img = Image.open(io.BytesIO(requests.get(msg.attachments[0]['url']).content)).convert('RGBA')
            tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(tmp)
            draw.rectangle((0, 0) + img.size, fill=(85, 26, 139, 175))

            img = Image.alpha_composite(img, tmp)
            imgbytearr = io.BytesIO()
            img.save(imgbytearr, format='PNG')
            imgbytearr = imgbytearr.getvalue()
            await client.send_file(msg.channel, io.BytesIO(imgbytearr), filename='its-purple.png')
        except IndexError:
            await client.send_message(msg.channel, 'You must attach a file')


client.run(os.environ["bot_token"])
