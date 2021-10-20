# bot.py
import logging
import os  # for importing env vars for the bot to use
import sys
from pathlib import Path

from twitchio import Channel, Client, User
from twitchio.ext import commands, pubsub


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
                # 'lickers__',
                'kingostone',
                # 'SeaBazT',
                'Hominidea',
                'kalderinofeross',
                'potdechoucroute',
            ]
        )
        self.pubsub_client = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.multipov_channels = ['smallpinkpanda', ]

    def setup(self):
        print("Chargement des cogs...")

        for cog in self._cogs_names:
            print(f" Loading `{cog}` cog.")
            self.load_module(f"cogs.{cog}")

        print("Chargement terminé")

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
        channel = self.pubsub_client.get_channel(
            os.environ['CHANNEL']
        )
        await channel.send("test")

    ## GENERAL FUNCTIONS ##

    @commands.command(name="salut")
    async def salut(self, ctx: commands.Context, *name):
        if not name:
            name = ctx.author.name
        else:
            name = name[0]
        await ctx.send(f'Salut @{name}!')

    @commands.command(name="git")
    async def git(self, ctx: commands.Context):
        await ctx.send(f'Here is my source code https://github.com/leochely/leixbot/ MrDestructoid')

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
            # await self.db.close()
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
        initial_channels=os.environ['CHANNEL'],
        client_secret=os.environ['CLIENT_SECRET']
    )

    client.pubsub = pubsub.PubSubPool(client)

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        await bot.event_pubsub_channel_points(event)

    bot = LeixBot()
    bot.pubsub_client = client
    bot.run()
