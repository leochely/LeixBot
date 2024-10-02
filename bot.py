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
from twitchio.ext import commands, routines, eventsub

from utils import auto_so, random_bot_reply, random_reply, play_alert
from db import init_channels, add_channel, leave_channel, get_channels_info, update_name


class LeixBot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.environ['ACCESS_TOKEN'],
            prefix=os.environ['BOT_PREFIX'],
            client_id=os.environ['CLIENT_ID'],
            initial_channels=init_channels(),
            case_insensitive=True
        )
        self.channel = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.vip_so = {
            x: {} for x in init_channels()
        }
        self.bot_to_reply = ['wizebot', 'streamelements', 'nightbot', 'moobot']
        self.routines = {}
        self.esclient = eventsub.EventSubWSClient(self)

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

        self.channel = self.get_channel(os.environ['CHANNEL'])

        # Retrieving routines from db
        self.routines = custom_commands.init_routines(self)

        # Starting timers
        logging.info("Starting routines...")
        self.links.start()
        self.id_updater.start()

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
            reply = custom_commands.get_command(message)
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
            await play_alert(channel.name, 'subscription', tags['display-name'])
        elif tags["msg-id"] == "resub":
            await channel.send(
                f"/me PogChamp Le resub de {tags['display-name']}!! Merci de fièrement soutenir la chaine depuis {tags['msg-param-cumulative-months']} mois <3"
            )
            await play_alert(channel.name, 'subscription', tags['display-name'])
        elif tags['msg-id'] == 'subgift':
            await channel.send(
                f'/me {tags["display-name"]} est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un sub!'
            )
            await play_alert(channel.name, 'subscription', tags['msg-param-recipient-display-name'])
        elif tags['msg-id'] == 'anonsubgift':
            await channel.send(
                f'/me Un donateur anonyme est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un sub!'
            )
            await play_alert(channel.name, 'subscription', tags['msg-param-recipient-display-name'])
        elif tags["msg-id"] == "raid":
            await channel.send(
                f"/me Il faut se défendre SwiftRage ! Nous sommes raid par {tags['msg-param-displayName']} et ses {tags['msg-param-viewerCount']} margoulins!"
            )
            await play_alert(channel.name, tags["msg-id"], tags['msg-param-displayName'])

    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            logging.error("Command does not exist")


    ## EVENTSUB WS FUNCTIONS ##
    async def event_eventsub_notification(self, payload: eventsub.NotificationEvent) -> None:
        print('Received event!')
        print(payload.headers.message_id)   
        
    async def event_eventsub_notification_channel_reward_redeem(self, payload: eventsub.CustomRewardRedemptionAddUpdateData) -> None:
        print('Received event!')
        print(payload.data.id)   


    async def event_eventsub_notification_stream_start(self, payload: eventsub.StreamOnlineData) -> None:
        print('Received event!')
        print(payload)
              

    async def event_eventsub_notification_followV2(self, payload: eventsub.ChannelFollowData) -> None:
        print('Received event!')
        print(f'{payload.data.user.name} followed woohoo!')

    async def event_eventsub_notification_channel_update(self, payload: eventsub.ChannelUpdateData) -> None:
        print('Received event!')
        print(payload)


    async def sub(self):
        await self.esclient.subscribe_channel_points_redeemed(broadcaster=self.channel, token=os.environ['CHANNEL_ACCESS_TOKEN'],)
        await self.esclient.subscribe_channel_stream_start(broadcaster=self.channel, token=os.environ['CHANNEL_ACCESS_TOKEN'])
        await self.esclient.subscribe_channel_update(broadcaster=self.channel, token=os.environ['CHANNEL_ACCESS_TOKEN'])
        await self.esclient.subscribe_channel_follows_v2(broadcaster=self.channel, moderator=self.channel, token=os.environ['CHANNEL_ACCESS_TOKEN'])

    ## ROUTINES ##
    @routines.routine(minutes=30.0, wait_first=False)
    async def links(self):
        await self.channel.send("Mon YouTube: https://youtube.com/leix34")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Guide Apex Legends: https://leochely.github.io/apexLegendsGuide/")
        await asyncio.sleep(60 * 30)
        await self.channel.send("Le discord: https://discord.com/invite/jzU7xWstS9")
        await asyncio.sleep(60 * 30)
        await self.channel.send("La radio Guilty, 24h/24 et 7j/7 sur https://www.youtube.com/@leix34/live ")
        await asyncio.sleep(60 * 30)

    @routines.routine(hours=1.0, wait_first=False)
    async def id_updater(self):
        channels_info = get_channels_info()
        channels = await self.fetch_channels(channels_info.keys())
        for channel in channels:
            user = await channel.user.fetch()
            if user.name != channels_info[channel.user.id]:
                update_name(channel.user.id, user.name)

    @commands.command(name="routineAdd")
    async def routine_add(self, ctx: commands.Context, name, seconds, minutes, hours, *text):
        """Ajoute et démarre une routine. Requiert privilege modérateur.
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

    @commands.command(name='commandes', aliases=['commands'])
    async def commandes(self, ctx: commands.Context):
        """
        Retourne la liste des commandes de LeixBot sur cette chaine
        """
        channel = ctx.author.channel.name
        commands = custom_commands.find_commands_channel(channel)

        cmd_list = ""
        for command in commands:
            cmd_list += command[0] + ", "

        # Remove last comma and space
        cmd_list = cmd_list[:-2]
        await ctx.send(
            f'La liste de mes commandes sur ce chat: {cmd_list}'
        )

    @commands.command(name="list")
    async def list(self, ctx: commands.Context):
        """
        Retourne la liste des commandes globales de LeixBot
        """

        cmd_list = ""
        for command in self.commands:
            cmd_list += command + ", "

        # Remove last comma and space
        cmd_list = cmd_list[:-2]
        await ctx.send(f'La liste des commandes globales de LeixBot: {cmd_list}')

    @commands.command(name="help")
    async def help(self, ctx: commands.Context, name):
        """Fournit l'aide d'une commande globale. Ex: !help help"""
        if name in self.commands:
            await ctx.send(self.commands[name]._callback.__doc__)
        else:
            await ctx.send("Désolé, ce n'est pas une de mes commandes globales :(")

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


    bot = LeixBot()
    bot.loop.create_task(bot.sub())
    bot.run()
