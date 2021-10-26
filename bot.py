# bot.py
import asyncio
import logging
import os  # for importing env vars for the bot to use
import sys
from datetime import datetime, timedelta
from pathlib import Path

from twitchio import Channel, Client, User
from twitchio.ext import commands, pubsub, routines


class LeixBot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(
            # set up the bot
            token=os.environ['ACCESS_TOKEN'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=[
                'leix34',
                'smallpinkpanda',
                'lickers__',
                'kingostone',
                # 'SeaBazT',
                'Hominidea',
                'kalderinofeross',
                'potdechoucroute',
                'zenoxyde'
            ],
            case_insensitive=True
        )
        self.pubsub_client = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.multipov_channels = ['smallpinkpanda', ]

    def setup(self):
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
        c: Channel = self.connected_channels[0]
        u: List["User"] = await self.fetch_users(names=[c.name])
        uu: User = u[0]

        topics = [pubsub.channel_points(self.pubsub_client._http.token)[uu.id]]
        await self.pubsub_client.pubsub.subscribe_topics(topics)
        await self.pubsub_client.connect()

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

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    ## PUBSUB FUNCTIONS ##
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        logging.info(
            f'Redemption by {event.user.name} of reward {event.reward.title} '
            f'with text {event.reward.prompt} done'
        )
        channel = self.pubsub_client.get_channel("leix34")
        if event.reward.title == "Hats off to you":
            minutes = 5
            time = datetime.now() + timedelta(minutes=minutes)
            await channel.send(f"Met le casque jusqu'à {time.strftime('%H:%M:%S')}")
            await asyncio.sleep(minutes * 60)
            await channel.send("/me @Leix34 tu peux maintenant retirer le casque")

    ## TIMERS ##
    @routines.routine(minutes=30.0, wait_first=False)
    async def links(self):
        channel = self.get_channel('leix34')
        await channel.send("Mon YouTube: https://youtube.com/leix34")
        await asyncio.sleep(60 * 30)
        await channel.send("Guide Apex Legends: https://leochely.github.io/apexLegendsGuide/")
        await asyncio.sleep(60 * 30)
        await channel.send("Le discord: https://leochely.github.io/apexLegendsGuide/")
        await asyncio.sleep(60 * 30)

    ## GENERAL FUNCTIONS ##
    @commands.command(name="salut")
    async def salut(self, ctx: commands.Context, *name):
        if not name:
            name = ctx.author.name
        else:
            name = name[0]
            if name[0] != '@':
                name = '@' + name
        await ctx.send(f'Salut {name}!')

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
        list = list[:-2]
        await ctx.send(f'La liste des commandes de LeixBot: {list}')

    @commands.command(name="shutdown")
    async def shutdown_command(self, ctx: commands.bot.Context):
        if ctx.author.is_mod:
            await ctx.send(f"LeixBot is now shutting down.")
            await self.close()
            sys.exit(0)


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
        initial_channels=['leix34'],
        client_secret=os.environ['CLIENT_SECRET']
    )

    client.pubsub = pubsub.PubSubPool(client)

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        await bot.event_pubsub_channel_points(event)

    bot = LeixBot()
    bot.pubsub_client = client
    bot.run()
