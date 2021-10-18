# bot.py
import logging
import os  # for importing env vars for the bot to use
import sys
from pathlib import Path

import cogs
from twitchio.ext import commands


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
                'kalderinofeross'
            ]
        )
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
        # We are logged in and ready to chat and use commands...
        logging.info(f'Logged in as | {self.nick}')

    # async def event_join(self, channel, user):
    #     # Notify us when everything is ready!
    #     # We are logged in and ready to chat and use commands...
    #     self.channel: twitchio.Channel = self.get_channel(channel.name)
    #     await self.channel.send("LeixBot is now online!")
    #     logging.info(f'Joined channel {channel}')

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

    @commands.command(name="salut")
    async def salut(self, ctx: commands.Context):
        await ctx.send(f'Salut {ctx.author.name}!')

    @commands.command(name="dblade")
    async def dblade(self, ctx: commands.Context):
        await ctx.send(f'Je te dedicace cette dblade {ctx.author.name}!')

    @commands.command(name="boubou")
    async def boubou(self, ctx: commands.Context):
        await ctx.send(f'Désolé @Lickers__!')

    @commands.command(name="fx")
    async def fx(self, ctx: commands.Context):
        await ctx.send('Kel bo fx')

    @commands.command(name="so")
    async def so(self, ctx: commands.Context):
        await ctx.send('yapadeso')

    @commands.command(name="porte")
    async def porte(self, ctx: commands.Context):
        await ctx.send("Vision d'artiste")

    @commands.command(name="den")
    async def den(self, ctx: commands.Context):
        await ctx.send('https://discord.gg/PEfEVWacgP')

    @commands.command(name="ref")
    async def ref(self, ctx: commands.Context):
        await ctx.send('glaref leix34Trigerred')

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
    bot = LeixBot()
    bot.run()
