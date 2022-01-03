import random
import re
from datetime import datetime, timedelta

from twitchio.ext import commands


async def auto_so(bot, message, vip_info):
    vip_name = message.author.name
    channel_info = await bot.fetch_channel(message.author.name)
    if (vip_name in vip_info and vip_info[vip_name] == datetime.now().date()) or 'vip' not in message.author.badges:
        return

    # Update last automatic shoutout time
    vip_info[message.author.name] = datetime.now().date()

    # Send message
    if channel_info.game_name:
        await message.author.channel.send(
            f'Allez voir @{vip_name} à www.twitch.tv/{vip_name} pour du gaming de qualitay sur {channel_info.game_name}'
        )
    else:
        await message.author.channel.send(
            f"@{vip_name} ne stream pas mais c'est quelqu'un de super cool SeemsGood"
        )


async def random_reply(message):
    compiled_msg = re.compile(re.escape("@leixbot"), re.IGNORECASE)
    msg_clean = compiled_msg.sub("", message.content)
    reply_pool = [
        "wsh t ki", "DONT LOOK BACK",
        "leix34Trigerred",
        "Oui vous m'avez demandé?",
        f"Ah ouais {msg_clean} ??"
    ]
    reply = random.choice(reply_pool)
    await message.author.channel.send(f"@{message.author.name} {reply}")


async def random_bot_reply(message):
    reply_pool = [
        f"wsh t ki @{message.author.name} DarkMode",
        f"LeixBot > {message.author.name} SwiftRage",
        f"tg {message.author.name} MrDestructoid",
        f"#LeixBotOnly, pas besoin de toi @{message.author.name}"
    ]
    reply = random.choice(reply_pool)
    await message.author.channel.send(f"{reply}")
