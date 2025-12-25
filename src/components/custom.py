import logging

from twitchio import User
from twitchio.ext import commands

import custom_commands

LOGGER: logging.Logger = logging.getLogger("Components.Custom")

class CustomCommand(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod

    @commands.is_moderator()
    @commands.command(name="cmdadd")
    async def cmdadd(self, ctx: commands.Context, command, *text):
        """Ajoute une commande a la base de données.
        Ex: !cmdadd !test ma commande
        """
        channel_id = ctx.broadcaster.id
        text = ' '.join(text)

        await custom_commands.add_command(command, channel_id, text)

        await ctx.send(f"Commande {command} ajoutée avec succes SeemsGood")

    @commands.is_moderator()
    @commands.command(name="cmdedit")
    async def cmdedit(self, ctx: commands.Context, command, *text):
        """Edite une commande presente dans la base de données.
        Ex: !cmdedit !test mon nouveau texte de commande
        """
        channel_id = ctx.broadcaster.id
        text = ' '.join(text)

        await custom_commands.edit_command(command, channel_id, text)

        await ctx.send(f"Commande {command} éditée avec succes SeemsGood")

    @commands.is_moderator()
    @commands.command(name="cmdremove")
    async def cmdremove(self, ctx: commands.Context, command):
        """
        Retire une commande de la base de données.
        Ex: !cmdremove !test
        """
        channel_id = ctx.broadcaster.id

        await custom_commands.remove_command(command, channel_id)

        await ctx.send(f"Commande {command} retirée avec succes SeemsGood")
    
    @commands.is_moderator()
    @commands.command(name="disableautosovip")
    async def disableautosovip(self, ctx: commands.Context):
        """Désactive le shoutout automatique pour les VIP et modérateurs"""
        await custom_commands.update_vip_so(ctx.broadcaster.id, False)
        await ctx.send('Le so automatique a été désactivé SeemsGood')

    @commands.is_moderator()
    @commands.command(name="enableautosovip")
    async def enableautosovip(self, ctx: commands.Context):
        """Active le shoutout automatique pour les VIP et modérateurs"""
        await custom_commands.update_vip_so(ctx.broadcaster.id, True)
        await ctx.send('Le so automatique a été activé SeemsGood')

    @commands.is_moderator()
    @commands.command(name="disablebotreplies")
    async def disablebotreplies(self, ctx: commands.Context):
        """Désactive les réponses automatiques aux bots"""
        await custom_commands.update_bot_replies(ctx.broadcaster.id, False)
        await ctx.send('Les réponses automatiques aux bots ont été désactivées SeemsGood')

    @commands.is_moderator()
    @commands.command(name="enablebotreplies")
    async def enablebotreplies(self, ctx: commands.Context):
        """Active les réponses automatiques aux bots"""
        await custom_commands.update_bot_replies(ctx.broadcaster.id, True)
        await ctx.send('Les réponses automatiques aux bots ont été activées SeemsGood')


async def setup(bot: commands.AutoBot):
    await bot.add_component(CustomCommand(bot))
