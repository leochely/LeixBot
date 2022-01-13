# bot.py
import asyncio
import logging
import os  # for importing env vars for the bot to use
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from twitchio import Channel, Client, User
from twitchio.ext import commands, pubsub, routines
from utils import auto_so, random_bot_reply, random_reply


class LeixBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.environ['ACCESS_TOKEN'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=os.environ['INITIAL_CHANNELS'].split(', '),
            case_insensitive=True
        )
        self.pubsub_client = None
        self.channel = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.vip_so = {
            x: {} for x in os.environ['INITIAL_CHANNELS'].split(', ')
        }
        self.bot_to_reply = ['wizebot', 'streamelements', 'nightbot', 'moobot']

    def setup(self):
        random.seed()

        print("Chargement des cogs...")

        for cog in self._cogs_names:
            logging.info(f"Loading `{cog}` cog.")
            self.load_module(f"cogs.{cog}")

        # logging.info("Starting timers")
        # self.loop.create_task(self.timers())

        logging.info("Chargement terminé")

    def run(self):
        self.setup()
        super().run()

    async def event_ready(self):
        # Notify us when everything is ready!

        # Subscribes through pubsub to topics
        u: List["User"] = await self.fetch_users(names=[os.environ['CHANNEL']])
        uu: User = u[0]

        topics = [
            pubsub.channel_points(self.pubsub_client._http.token)[uu.id],
            pubsub.bits(self.pubsub_client._http.token)[uu.id]
        ]
        await self.pubsub_client.pubsub.subscribe_topics(topics)
        await self.pubsub_client.connect()
        self.channel = self.get_channel(os.environ['CHANNEL'])

        # Starting timers
        self.links.start()

        # We are logged in and ready to chat and use commands...
        logging.info(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        logging.info(
            f'{message.author.name} on channel {message.author.channel.name}: '
            f'{message.content}'
        )

        if "@leixbot" in message.content.lower():
            await random_reply(self, message)
        elif message.author.name.lower() in self.bot_to_reply:
            await random_bot_reply(message)
        else:
            await auto_so(self, message, self.vip_so[message.author.channel.name])

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def event_raw_usernotice(self, channel, tags):
        logging.debug(tags)
        if tags["msg-id"] == "sub":
            await channel.send(f"/me PogChamp {tags['display-name']} rejoint la légion! Merci pour le sub PogChamp")
        elif tags["msg-id"] == "resub":
            await channel.send(
                f"/me PogChamp Le resub de {tags['display-name']}!! Merci de fièrement soutenir la chaine depuis {tags['msg-param-cumulative-months']} mois <3"
            )
        elif tags['msg-id'] == 'subgift':
            await channel.send(
                f'/me {tags["display-name"]} est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un sub!'
            )
        elif tags['msg-id'] == 'anonsubgift':
            await channel.send(
                f'/me AnAnonymousGifter est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un sub!'
            )
        elif tags["msg-id"] == "raid":
            await channel.send(
                f"/me Il faut se défendre SwiftRage ! Nous sommes raid par {tags['msg-param-displayName']} et ses {tags['msg-param-viewerCount']} margoulins!"
            )

    ## PUBSUB FUNCTIONS ##
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        logging.info(
            f'Redemption by {event.user.name} of reward {event.reward.title} '
            f'with input {event.input} done'
        )
        if event.reward.title == "Hats off to you":
            minutes = 5
            time = datetime.now() + timedelta(minutes=minutes)
            await self.channel.send(f"/me Met le casque jusqu'à {time.strftime('%H:%M:%S')}")
            await asyncio.sleep(minutes * 60)
            await channel.send("/me @Leix34 tu peux maintenant retirer le casque")

    async def event_pubsub_bits(self, event: pubsub.PubSubBitsMessage):
        logging.info(
            f'{event.user.name} just donated {event.bits_used} bits!'
        )
        self.channel.send(
            f'/me Merci pour les {event.bits_used} bits @{event.user.name} PogChamp'
        )

    ## TIMERS ##
    @routines.routine(minutes=30.0, wait_first=False)
    async def links(self):
        await self.channel.send("Mon YouTube: https://youtube.com/leix34")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Guide Apex Legends: https://leochely.github.io/apexLegendsGuide/")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Le discord: https://discord.com/invite/jzU7xWstS9")
        await asyncio.sleep(60 * 30)

    ## GENERAL FUNCTIONS ##
    @commands.command(name="git")
    async def git(self, ctx: commands.Context):
        await ctx.send(
            f'Here is my source code https://github.com/leochely/leixbot/ MrDestructoid'
        )

    @commands.command(name="list")
    async def list(self, ctx: commands.Context):
        list = ""
        for command in self.commands:
            list += command + ", "

        # Remove last comma and space
        list = list[:-2]
        await ctx.send(f'La liste des commandes de LeixBot: {list}')


if __name__ == "__main__":
    logging.basicConfig(
        encoding='utf-8',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

    client = Client(
        token=os.environ['CHANNEL_ACCESS_TOKEN'],
        initial_channels=os.environ['CHANNEL'],
        client_secret=os.environ['CLIENT_SECRET']
    )

    client.pubsub = pubsub.PubSubPool(client)

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        await bot.event_pubsub_channel_points(event)

    @client.event()
    async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
        await bot.event_pubsub_bits(event)

    bot = LeixBot()
    bot.pubsub_client = client
    bot.run()
