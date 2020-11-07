import img.external_images as external_images
import strings as strings

import io
import os
import random
import re

import asyncio
import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image, ImageDraw
import requests

client = discord.Client()

fb_creds = credentials.Certificate({
    "type": "service_account",
    "project_id": "kraft-punk-bot",
    "private_key_id": os.environ["fb_key_id"],
    "private_key": os.environ["fb_key"].replace(r'\n', '\n'),
    "client_email": os.environ["fb_email"],
    "client_id": os.environ["fb_client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ["fb_cert_url"]
})
firebase_admin.initialize_app(fb_creds)

db = firestore.client()


def message_has_trigger(msg, keyword):
    return re.search('\\b' + keyword + '\\b', msg.content.lower())


def message_mentions_bot(msg):
    return client.user.mentioned_in(msg)


async def channel_is_muted(server_id, channel_id):
    server_ref = db.collection(u'mutes').document(str(server_id))
    channel_ref = server_ref.collection(u'channels').document(str(channel_id))

    channel = channel_ref.get()

    return channel.get(u'muted')


async def mute_channel(server_id, channel_id):
    server_ref = db.collection(u'mutes').document(str(server_id))
    server_ref.collection(u'channels').document(str(channel_id)).set({
        u'muted': True
    })

    return


async def unmute_channel(server_id, channel_id):
    server_ref = db.collection(u'mutes').document(str(server_id))
    server_ref.collection(u'channels').document(str(channel_id)).set({
        u'muted': False
    })

    return


async def send_image(channel, img, caption=''):
    await channel.send(file=discord.File('./img/' + img), content=caption)


async def send_message(channel, msg):
    await channel.send(msg)


async def get_last_image_from_channel(channel):
    async for m in channel.history():
        if m.attachments:
            try:
                Image.open(io.BytesIO(requests.get(m.attachments[0].url).content)).convert('RGBA')
                return m
            except OSError:
                # Not an image attachment
                continue

    return None


async def make_image_purple(img):
    tmp = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(tmp)
    draw.rectangle((0, 0) + img.size, fill=(85, 26, 139, 175))

    img = Image.alpha_composite(img, tmp)
    imgbytearr = io.BytesIO()
    img.save(imgbytearr, format='PNG')
    imgbytearr = imgbytearr.getvalue()
    return io.BytesIO(imgbytearr)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(msg):
    if message_mentions_bot(msg) and message_has_trigger(msg, 'mute'):
        await mute_channel(msg.guild.id, msg.channel.id)
        await send_message(msg.channel, "Muted in this channel")

    elif message_mentions_bot(msg) and message_has_trigger(msg, 'unmute'):
        await unmute_channel(msg.guild.id, msg.channel.id)
        await send_message(msg.channel, "Un-muted in this channel")

    elif await channel_is_muted(msg.guild.id, msg.channel.id):
        return

    elif msg.author.id == client.user.id:
        return

    elif message_mentions_bot(msg) and message_has_trigger(msg, '(thanks|thank you)'):
        await send_message(msg.channel, "You're welcome " + msg.author.mention)

    elif message_has_trigger(msg, 'what if it (was|were) purple'):
        attachment = None

        try:
            attachment = msg.attachments[0].url
        except IndexError:
            try:
                last_msg = await get_last_image_from_channel(msg.channel)
                attachment = last_msg.attachments[0].url
            except (IndexError, AttributeError):
                await msg.channel.send('Nothing to make purple!')

        if attachment is not None:
            try:
                img = Image.open(io.BytesIO(requests.get(attachment).content)).convert('RGBA')
                await msg.channel.send(file=discord.File(await make_image_purple(img), 'its-purple.png'))
            except OSError:
                await msg.channel.send('Looks like the last sent file isn\'t an image!')

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

    elif message_has_trigger(msg, 'call me'):
        await send_image(msg.channel, 'callme.jpg')

    elif message_has_trigger(msg, 'coachella'):
        await send_image(msg.channel, 'coachella.png')

    elif message_has_trigger(msg, '(catch the excitement|excited)'):
        await send_image(msg.channel, 'excitement.png')

    elif message_has_trigger(msg, '(froot|fruit) loops'):
        await send_image(msg.channel, 'frootloops.png')

    elif message_has_trigger(msg, '(frozen (yogurt|yoghurt)|froyo)'):
        await send_image(msg.channel, 'froyo.png', caption=random.choice(strings.froyo_captions))

    elif message_has_trigger(msg, '(gas|gasoline|petrol|fuel)'):
        await send_image(msg.channel, 'gas.png')

    elif message_mentions_bot(msg) and message_has_trigger(msg, '(help|what\'s up)'):
        await send_image(msg.channel, 'heywhatsup.png',
                         caption="Hey what's up? I'm Kraft Punk! Did you guys know I cannot die?")
        await send_message(msg.channel, "I'll just be here waiting to drop into the conversation with some "
                                        "pics from the Eric Andre show")
        await send_message(msg.channel, "See you later!")

    elif message_mentions_bot(msg) and message_has_trigger(msg, '(can you leave|leave|get out of here|please leave)'):
        await send_image(msg.channel, 'leaving.png', caption='Okay, bye!')

    elif message_has_trigger(msg, 'let me in'):
        base = Image.open('./img/letmein.jpg')
        avatar = Image.open(io.BytesIO(requests.get(msg.author.avatar_url).content))

        avatar_sm = avatar.resize((100, 100))
        avatar_lg = avatar.resize((240, 240))

        base.paste(avatar_sm, box=(344, 116))
        base.paste(avatar_lg, box=(506, 440))

        edited_base_bytes = io.BytesIO()
        base.save(edited_base_bytes, format="JPEG")
        edited_base_bytes = edited_base_bytes.getvalue()
        base.close()

        await msg.channel.send(file=discord.File(io.BytesIO(edited_base_bytes), 'letmein.jpg'))

    elif message_has_trigger(msg, 'questlove'):
        if message_has_trigger(msg, "questlove you're not in the house"):
            await send_image(msg.channel, 'notinthehouse.png', caption="You're nowhere")
        else:
            await send_image(msg.channel, 'questlove.png',
                             caption="Hey " + msg.author.mention + "! Questlove's in the house!")

    elif message_has_trigger(msg, '((order|get) pizzas?|(order|get) some pizzas?|order a pizza|pizza delivered)'):
        await send_image(msg.channel, 'pizza.jpg', caption="TIME TO DELIVER A PIZZA BALL")

    elif message_has_trigger(msg, 'ranch'):
        await send_image(msg.channel, 'ranch.jpg')

    elif message_has_trigger(msg, '(get yourself together|move to (philly|philadelphia)|philly|philadelphia|hummus)'):
        await send_message(msg.channel, external_images.philly)

    elif message_has_trigger(msg, 'rice'):
        await send_image(msg.channel, 'rice.png')

    elif message_has_trigger(msg, '(scientology|l.? ron hubbard|lrh|hubbard)'):
        await send_image(msg.channel, 'scientology.png', caption='There is no hell!')

    elif message_has_trigger(msg, 'so controversial (yet|but) so brave\\??'):
        await send_image(msg.channel, 'sobrave.gif')

    elif any(message_has_trigger(msg, trigger) for trigger in strings.thetits_triggers):
        await send_image(msg.channel, 'thetits.png')

    elif message_has_trigger(msg, 'wheel of prizes'):
        await send_message(msg.channel, "It's time for the Wheel of Prizes!\n" + external_images.wheel_intro)
        await asyncio.sleep(1)
        await send_message(msg.channel, external_images.wheel_spin)
        await asyncio.sleep(1)
        await send_message(msg.channel, external_images.wheel_spinning)
        await asyncio.sleep(5)
        await send_message(msg.channel, msg.author.mention + ' you won: ' + random.choice(strings.prizes))

    elif any(message_has_trigger(msg, trigger) for trigger in strings.wth_triggers):
        await send_image(msg.channel, 'wth.gif')

    elif message_has_trigger(msg, '(scream|screaming)'):
        await send_image(msg.channel, 'screamtime.png')

    elif message_has_trigger(msg, 'lizzo'):
        await send_image(msg.channel, 'lizzo.png')

    elif message_has_trigger(msg, '(ice cream|icecream)'):
        await send_image(msg.channel, 'icecream.png')

    elif message_has_trigger(msg, 'lo mein'):
        await send_image(msg.channel, 'lomein.png')

    elif message_has_trigger(msg, '(brb|be right back)'):
        await send_image(msg.channel, 'brb/' + random.choice(os.listdir('./img/brb')))


client.run(os.environ["bot_token"])
