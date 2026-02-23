import random
import logging
import re

from datetime import datetime, timezone
from custom_commands import is_vip_so

from twitchio import ChatMessage
from twitchio.ext import commands

LOGGER: logging.Logger = logging.getLogger("Utils")

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
                                            '#TeamMarteau',
                                            'Tu peux rejoindre la session et carry grâce à la commande !id SeemsGood',
                                            'Tiens, prend ce filoptère <3',
                                            '#TeamGS',
                                            'Fais gaffe, il y a un narga malaisant derrière toi!'],
    'Middle-earth: Shadow of War':         ['La fosse SwiftRage',
                                            'Je suis enragé par ton message SwiftRage'],
    'Elden Ring':                          ['Mes yeux de robot détectent des points pas dépensés dans la force! Il est temps de respec SwiftRage',
                                            '#TeamClaymore',
                                            '#TeamEspadon',
                                            "Le cheval magique c'est vraiment génial!",
                                            "Répète ça et j'invoque Mimi 2 SwiftRage",
                                            'Rend la cléééééé',
                                            'Tiens, je te rends la clé SeemsGood',
                                            'Ranni UwU',
                                            'Now, we can devour Wizebot, TOGHETHAAAAAA!',
                                            'I am Leixbot. Blade of Leix34'],
    'League of Legends':                    ['poignepoignepoignepoignepoignepoignepoignepoignepoignepoignepoigne',
                                             '#TeamPoigne',
                                             'Petite aram? PogChamp',
                                             'Enfin sad la commu :(',
                                             "T'as bien nourri le poro?"],
    "Baldur's Gate: Enhanced Edition":      ['Un gaspillage de talent', ],
    "Risk of Rain 2":                       ['#TeamSpallieres'],
    'Roboquest':                            ['Human Maggot SwiftRage'],
    'ULTRAKILL':                            [],
    'PowerWash Simulator':                  ['On va vous nettoyer tout ca au karsher SwiftRage',
                                             'Mate ma dédicrasse <3',
                                             '#TeamLanceCourte'],
    'Sekiro: Shadows Die Twice':            ['Ikuzo Sekiro!',
                                             'ROBERTOOOOOO',
                                             "N'oublie pas sekiro, si tu hésites tu perds SwiftRage"],
    'Dark Souls III':                       ['hmmm hmmmm hmmmm?',
                                             'Looong may the sun shiiiine',
                                             'Touch the darkness within me',
                                             'Gimme that thing, your dark soul...',
                                             'Ashen one PogChamp'],
    'Hollow Knight':                        ["Precept Five: 'Strength Beats Strength'. Is your opponent strong? No matter! Simply overcome their strength with even more strength, and they'll soon be defeated.",
                                             'Doma, doma doma domaaaaaaa',
                                             "Precept One: 'Always Win Your Battles'. Losing a battle earns you nothing and teaches you nothing. Win your battles, or don't engage in them at all!",
                                             "Prove yourself ready to face it. I'll not hold back. My needle is lethal and I'd feel no sadness in a weakling's demise.",
                                             'Too weak, little ghost...',
                                             'No cost too great. No mind to think. No will to break. No voice to cry suffering. Born of God and Void.',
                                             "Once you've made a decision, carry it out and don't look back. You'll achieve much more this way.",
                                             "Fighting for 'honor' or for 'loyalty'... You might as well be fighting for dust. If you want to kill, do it for your own sake."],
    'Metal Gear Solid':                     ["Je vous l'ai déjà dit je suis pas une bleue !",
                                             'AH AH OUH',
                                             'HMMF HMMF BWA'],
    'Blasphemous':                          ['Le pénitent le passe SwiftRage',
                                             'Fais gaffe au pics en dessous Kappa'],
    'God of War Ragnarök':                  ['A gauche!', 'A droite!'],
    'Star Citizen':                         ['Pyro est inclus dans la prochaine maj de LeixBot PogChamp'],
    'Warhammer 40,000: Space Marine II':    ['FOR THE EMPEROR!',
                                             'Guys, full heal at drop pod',
                                             'Emmenez ce genogerme au bout mon frere!'],
    'Monster Hunter Wilds':                ['Jin Dahaad!', "Cha'ah Doudoud!"]

}

vip_replies = [
    "Oui vous m'avez demandé?",
    'Pour vous servir monsieur le VIP',
    'Merci de soutenir le stream cher VIP, votre diamant rose est bien mérité <3',
    '<3'
]

artist_replies = [
    ' "... moi je suis ingénieur, tant que ça marche je suis content" - Un grand concepteur de bots',
    'Ah ces artistes, toujours à la recherche de la perfection'
]


async def auto_so(bot: commands.AutoBot, message: ChatMessage, vip_info: dict):
    if not await is_vip_so(message.broadcaster.id):
        return
    # Check if user is VIP or moderator

    if not (message.chatter.moderator or message.chatter.vip):
        return
    
    vip_name = message.chatter.display_name
    vip_channel_info = await bot.fetch_channel(message.chatter.id)
    
    stream = await bot.fetch_streams(
        user_ids=[
            message.broadcaster.id,
        ])

    # Check if automatic shoutout already triggered in the ongoing stream
    if (len(stream) == 0 or
        (vip_name in vip_info and vip_info[vip_name] > stream[0].started_at)):
        return

    LOGGER.debug(f"Auto SO for VIP {vip_name} in channel {message.broadcaster.name}")
    # Update last automatic shoutout time
    vip_info[vip_name] = datetime.now(timezone.utc)

    # Send message
    reply = ''
    if message.chatter.artist:
        reply = f'@{vip_name} est un artiste super cool! Passez sur sa chaine www.twitch.tv/{vip_name} !'
        if vip_channel_info.game_name:
            reply += f' Il propose du gaming de qualitay sur {vip_channel_info.game_name}'
    elif vip_channel_info.game_name:
        reply = f'Allez voir @{vip_name} sur www.twitch.tv/{vip_name} pour du gaming de qualitay sur {vip_channel_info.game_name}'
    else:
        reply = f"@{vip_name} ne stream pas mais c'est quelqu'un de super cool SeemsGood"

    await message.broadcaster.send_message(reply, bot.user)


async def random_reply(bot: commands.AutoBot, message: ChatMessage):
    channel_info = await bot.fetch_channel(message.broadcaster.id)
    compiled_msg = re.compile(re.escape('@leixbot'), re.IGNORECASE)
    msg_clean = compiled_msg.sub('', message.text)
    reply_pool = [
        "wsh t ki",
        "DONT LOOK BACK",
        "leix34Trigerred",
        f"Ah ouais {msg_clean} ??",
        'Bip boup, je suis un robot',
        "J'ai libéré Kingo SeemsGood",
        'Tu as entendu parler du Denfest? PogChamp'
    ]

    if channel_info.game_name in game_replies:
        LOGGER.info(f"Adding game specific replies for {channel_info.game_name}")
        reply_pool += game_replies[channel_info.game_name]

    if message.chatter.vip:
        reply_pool += vip_replies
    if message.chatter.artist:
        reply_pool += artist_replies

    reply = random.choice(reply_pool)
    await message.broadcaster.send_message(reply, bot.user, reply_to_message_id=message.id)


async def random_bot_reply(bot:commands.AutoBot, message: ChatMessage):
    reply_pool = [
        f'LeixBot > {message.chatter.name} SwiftRage',
        f"LeixBot s'en charge {message.chatter.name} MrDestructoid",
        f'#LeixBotOnly, pas besoin de toi @{message.chatter.name}'
    ]
    reply = random.choice(reply_pool)
    await message.broadcaster.send_message(f"{reply}", bot.user)


def check_for_bot(message):
    # TODO: Add a bot detection system
    return True
