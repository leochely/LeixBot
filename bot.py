# bot.py
import asyncio
import logging
import os  # for importing env vars for the bot to use
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import custom_commands
from twitchio import Channel, Client, User
from twitchio.ext import commands, pubsub, routines

from utils import auto_so, check_for_bot, random_bot_reply, random_reply, play_alert
from db import init_channels, add_channel, leave_channel


class LeixBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.environ['ACCESS_TOKEN'],
            prefix=os.environ['BOT_PREFIX'],
            client_id=os.environ['CLIENT_ID'],
            initial_channels=init_channels(),
            case_insensitive=True
        )
        self.pubsub_client = None
        self.channel = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.vip_so = {
            x: {} for x in init_channels()
        }
        self.bot_to_reply = ['wizebot', 'streamelements', 'nightbot', 'moobot']
        self.giveaway = set()
        self.routines = {}

    def setup(self):
        random.seed()
        logging.info("Chargement des cogs...")

        for cog in self._cogs_names:
            logging.info(f"Loading `{cog}` cog.")
            self.load_module(f"cogs.{cog}")

        logging.info("Chargement terminé")

        # Retrieving custom commands from db
        custom_commands.init_commands()

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

        # Retrieving routines from db
        self.routines = custom_commands.init_routines(self)

        # Starting timers
        logging.info("Starting routines...")
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

        ctx = await self.get_context(message)

        # if check_for_bot(message.content):
        #     logging.info("BOT DETECTED")
        #     message.author.channel.send(
        #         f'/ban {message.author.name} Vilain Bot')

        if message.content[0] == os.environ['BOT_PREFIX']:
            reply = custom_commands.find_command(message)
            if reply is not None:
                await ctx.reply(reply)
                return

        if "@leixbot" in message.content.lower():
            await random_reply(self, message)
        elif message.author.name.lower() in self.bot_to_reply and custom_commands.is_bot_reply(ctx.author.channel.name):
            await random_bot_reply(message)
        else:
            await auto_so(self, message, self.vip_so[message.author.channel.name])

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def event_raw_usernotice(self, channel, tags):
        if tags["msg-id"] == "sub":
            await channel.send(f"/me PogChamp {tags['display-name']} rejoint la légion! Merci pour le sub PogChamp")
            await play_alert(channel.name, tags["msg-id"])
        elif tags["msg-id"] == "resub":
            await channel.send(
                f"/me PogChamp Le resub de {tags['display-name']}!! Merci de fièrement soutenir la chaine depuis {tags['msg-param-cumulative-months']} mois <3"
            )
            await play_alert(channel.name, tags["msg-id"])
        elif tags['msg-id'] == 'subgift':
            await channel.send(
                f'/me {tags["display-name"]} est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un sub!'
            )
            await play_alert(channel.name, tags["msg-id"])
        elif tags['msg-id'] == 'anonsubgift':
            await channel.send(
                f'/me Un donateur anonyme est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un sub!'
            )
            await play_alert(channel.name, tags["msg-id"])
        elif tags["msg-id"] == "raid":
            await channel.send(
                f"/me Il faut se défendre SwiftRage ! Nous sommes raid par {tags['msg-param-displayName']} et ses {tags['msg-param-viewerCount']} margoulins!"
            )
            await play_alert(channel.name, tags["msg-id"])

    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            logging.error("Command does not exist")

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
            await self.channel.send("/me @Leix34 tu peux maintenant retirer le casque")

        if event.reward.title == "Giveaway":
            logging.info(f'{event.user.name} entered the giveaway!')
            self.giveaway.add(event.user.name)

    async def event_pubsub_bits_message(self, event: pubsub.PubSubBitsMessage):
        logging.info(
            f'{event.user} redeemed {event.bits_used} with message {event.message}'
        )
        await self.channel.send(f'Merci pour les {event.bits_used} bits @ {event.user.name} <3')

    ## ROUTINES ##
    @routines.routine(minutes=30.0, wait_first=False)
    async def links(self):
        await self.channel.send("Mon YouTube: https://youtube.com/leix34")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Guide Apex Legends: https://leochely.github.io/apexLegendsGuide/")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Le discord: https://discord.com/invite/jzU7xWstS9")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Un giveaway de jeux est en cours! Pour 5k slayer points, vous pouvez avoir une chance de remporter un des jeux du giveaway (liste complete dans la recompense de chaine)")
        await asyncio.sleep(60 * 30)

    @commands.command(name="routineAdd")
    async def routine_add(self, ctx: commands.Context, name, seconds, minutes, hours, *text):
        """Ajoute de demarre une routine une routine. Requiert privilege modérateur.
        Ex: !routineAdd mon_nom_de_routine 1 2 3 Mon texte de routine
        """
        if not ctx.author.is_mod:
            return

        routine_text = ' '.join(text)

        channel = self.get_channel(ctx.author.channel.name)

        logging.info(channel)

        @routines.routine(seconds=int(seconds), minutes=int(minutes), hours=int(hours), wait_first=False)
        async def temp_routine():
            await channel.send(routine_text)

        # Starts routine
        self.routines[ctx.author.channel.name + '_' + name] = temp_routine
        self.routines[ctx.author.channel.name + '_' + name].start()

        # Adds routine to db
        custom_commands.add_routine(
            ctx.author.channel.name,
            name,
            seconds,
            minutes,
            hours,
            routine_text
        )
        await ctx.send('Routine créée avec succès SeemsGood')

    @commands.command(name="routineStop")
    async def routine_stop(self, ctx: commands.Context, name):
        """Arrete et supprime une routine. Requiert privilege modérateur.
        Ex: !routineStop ma_routine
        """
        if not ctx.author.is_mod:
            return

        # Stops routine
        self.routines[ctx.author.channel.name + '_' + name].cancel()

        # Removes routine from db
        custom_commands.remove_routine(ctx.author.channel.name, name)
        await ctx.send('Routine stoppée avec succès MrDestructoid')

    ## GENERAL FUNCTIONS ##
    @commands.command(name="git")
    async def git(self, ctx: commands.Context):
        """Renvoie le lien vers le repo GitHub de LeixBot. Ex: !git"""
        await ctx.send(
            f'Here is my source code https://github.com/leochely/leixbot/ MrDestructoid'
        )

    @commands.command(name="list")
    async def list(self, ctx: commands.Context):
        """
        Retourne la liste des commandes globales de LeixBot
        """

        list = ""
        for command in self.commands:
            list += command + ", "

        # Remove last comma and space
        list = list[:-2]
        await ctx.send(f'La liste des commandes de LeixBot: {list}')

    @commands.command(name="help")
    async def help(self, ctx: commands.Context, name):
        """Fourni l'aide d'une commande globale. Ex: !help help"""
        if name in self.commands:
            await ctx.send(self.commands[name]._callback.__doc__)
        else:
            await ctx.send("Désolé, ce n'est pas une de mes commande globale :(")

    @commands.command(name="join")
    async def join(self, ctx: commands.Context, channel):
        """Envoie LeixBot sur votre chaine. Ex: !join ma_chaine"""
        if ctx.author.name == os.environ['CHANNEL'] or ctx.author.name == channel:
            channel = channel.lower()
            await ctx.send(f'Joining channel {channel}')

            await self.join_channels({channel})
            self.vip_so[channel] = {}
            add_channel(channel)

    @commands.command(name="leave")
    async def leave(self, ctx: commands.Context, channel):
        """Retire LeixBot de votre chaine. Ex: !leave ma_chaine"""
        if ctx.author.name == os.environ['CHANNEL'] or ctx.author.name == channel:
            channel = channel.lower()
            await ctx.send(f'Leaving channel {channel}')

            await self.part_channels({channel})
            leave_channel(channel)

    @commands.command(name="draw")
    async def draw(self, ctx: commands.Context):
        giveaway = list(self.giveaway)
        winners = random.sample(giveaway, k=5)
        games = ['SUPERHOT', 'Slay the spire',
                 'Tooth and Tail', 'Dear Esther', 'Max Payne 3']
        random.shuffle(games)
        for winner, game in zip(winners, games):
            await ctx.send(f'Félicitations {winner}! Tu as remporté {game}! SeemsGood')

    @commands.command(name="giveawayadd")
    async def giveawayadd(self, ctx: commands.Context, user: User = None):
        await ctx.send(f'{user.name} entered the giveaway!')
        self.giveaway.add(user.name)

    @commands.command(name="temp")
    async def temp(self, ctx: commands.Context, event):
        await play_alert(ctx.author.name, event)


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
        client_secret=os.environ['CLIENT_SECRET']
    )

    client.pubsub = pubsub.PubSubPool(client)

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        await bot.event_pubsub_channel_points(event)

    @client.event()
    async def event_pubsub_bits(event: pubsub.PubSubBitsMessage):
        await bot.event_pubsub_bits_message(event)

    bot = LeixBot()
    bot.pubsub_client = client
    bot.run()
