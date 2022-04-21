import random
import logging
import requests
import os
import re

from datetime import datetime, timedelta, timezone
from db import get_token

from twitchio.ext import commands


### Replies ###

game_replies = {
    'Guilty Gear: Strive':                 ['#10HitPetitPoingCombo',
                                            'MET TA GARDE',
                                            'Arrête de piffer tes ults SwiftRage',
                                            'Tu main Faust? leix34Trigerred',
                                            'Tu main Sol? <3',
                                            'Tu main May? WutFace',
                                            'DONT LOOK BACK SwiftRage',
                                            'Le choppeur fou PogChamp'],
    'Monster Hunter: World':               ['Arrête de critiquer les hitboxes stp Kappa',
                                            '#FixTheClaw',
                                            'Toi aussi tu aimes les monstres originaux comme le Fatalis? Kappa',
                                            "RisE C'eSt B1",
                                            'Tu peux rejoindre la session et carry grâce à la commande !id SeemsGood'],
    'DOOM Eternal':                        ['RIP AND TEAR leix34Trigerred',
                                            'Meurs démon SwiftRage',
                                            '#BloodPunchFixed', ],
    'Monster Hunter Generations Ultimate': ['Tu peux rejoindre avec la commande !id si tu as une GBA Kappa',
                                            "J'ai beau être un robot, j'ai mal aux yeux devant GU smallp9EuuuuuH",
                                            'Toi aussi tu es hébété devant le MALAISE du Tigrex??',
                                            "Je note ton message 6 sur l'échelle de MALAISE du Diablos Noir"],
    'Monster Hunter Rise':                 ['World > Rise Kappa',
                                            "Comment s'appelle ton palico? <3",
                                            "Comment s'appelle ton doggo? <3",
                                            '#TeamMarteau'],
    'Middle-earth: Shadow of War':         ['La fosse SwiftRage',
                                            'Je suis enragé par ton message SwiftRage'],
    'Elden Ring':                          ['Mes yeux de robot détectent des points pas dépensés dans la force! Il est temps de respec SwiftRage',
                                            '#TeamClaymore',
                                            '#TeamEspadon',
                                            "Le cheval magique c'est vraiment génial!",
                                            "Répète ça et j'invoque Mimi 2 SwiftRage"],
    'League of Legends':                    ['poignepoignepoignepoignepoignepoignepoignepoignepoignepoignepoigne',
                                             '#TeamPoigne',
                                             'Petite aram? PogChamp',
                                             'Enfin sad la commu :(',
                                             "T'as bien nourri le poro?"]
}

vip_replies = [
    "Oui vous m'avez demandé?",
    'Pour vous servir monsieur le VIP',
    'Merci de soutenir le stream cher VIP, votre diamant rose est bien mérité <3',
    '<3'
]


async def auto_so(bot, message, vip_info):
    vip_name = message.author.name
    vip_channel_info = await bot.fetch_channel(message.author.name)
    stream = await bot.fetch_streams(
        user_logins=[
            message.author.channel.name
        ])

    if len(stream) == 0 or (vip_name in vip_info and vip_info[vip_name] > stream[0].started_at) or ('vip' not in message.author.badges and 'moderator' not in message.author.badges):
        return

    # Update last automatic shoutout time
    vip_info[message.author.name] = datetime.now(timezone.utc)

    # Send message
    if vip_channel_info.game_name:
        await message.author.channel.send(
            f'Allez voir @{vip_name} sur www.twitch.tv/{vip_name} pour du gaming de qualitay sur {vip_channel_info.game_name}'
        )
    else:
        await message.author.channel.send(
            f"@{vip_name} ne stream pas mais c'est quelqu'un de super cool SeemsGood"
        )


async def random_reply(bot, message):
    channel_info = await bot.fetch_channel(message.channel.name)
    compiled_msg = re.compile(re.escape('@leixbot'), re.IGNORECASE)
    msg_clean = compiled_msg.sub('', message.content)
    reply_pool = [
        "wsh t ki",
        "DONT LOOK BACK",
        "leix34Trigerred",
        f"Ah ouais {msg_clean}??",
        'Bip boup, je suis un robot'
    ]
    if channel_info.game_name in game_replies:
        reply_pool += game_replies[channel_info.game_name]

    if 'vip' in message.author.badges:
        reply_pool += vip_replies

    reply = random.choice(reply_pool)
    await message.author.channel.send(f"@{message.author.name} {reply}")


async def random_bot_reply(message):
    reply_pool = [
        f'LeixBot > {message.author.name} SwiftRage',
        f"LeixBot s'en charge {message.author.name} MrDestructoid",
        f'#LeixBotOnly, pas besoin de toi @{message.author.name}'
    ]
    reply = random.choice(reply_pool)
    await message.author.channel.send(f"{reply}")


def check_for_bot(message):
    # TODO: Add a bot detection system
    return True


### API ###
base_url = "https://api.twitch.tv/helix/channels?broadcaster_id="


def modify_stream(user, game_id: int = None, language: str = None, title: str = None):
    url = base_url + str(user.id)
    auth = "Bearer " + get_token(user.name)
    id = os.environ['CLIENT_ID']

    headers = {
        "Client-Id": id,
        "Authorization": auth
    }

    data = {
        k: v
        for k, v in {"game_id": game_id, "broadcaster_language": language, "title": title}.items()
        if v is not None
    }

    resp = requests.patch(url, headers=headers, data=data)
    return resp.status_code == 204
