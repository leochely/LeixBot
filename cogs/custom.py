import datetime
import logging
import os

from twitchio import User
from twitchio.ext import commands

import custom_commands


class CustomCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.is_mod

    @commands.command(name="cmdadd")
    async def cmdadd(self, ctx: commands.Context, command, *text):
        """Ajoute une commande a la base de données.
        Ex: !cmdadd !test ma commande
        """
        channel = ctx.author.channel.name.lower()
        text = ' '.join(text)

        custom_commands.add_command(command, channel, text)

        await ctx.send(f"Commande {command} ajoutée avec succes SeemsGood")

    @commands.command(name="cmdedit")
    async def cmdedit(self, ctx: commands.Context, command, *text):
        """Edite une commande presente dans la base de données.
        Ex: !cmdedit !test mon nouveau texte de commande
        """
        channel = ctx.author.channel.name.lower()
        text = ' '.join(text)

        custom_commands.edit_command(command, channel, text)

        await ctx.send(f"Commande {command} éditée avec succes SeemsGood")

    @commands.command(name="cmdremove")
    async def cmdremove(self, ctx: commands.Context, command):
        """
        Retire une commande de la base de données.
        Ex: !cmdremove !test
        """
        channel = ctx.author.channel.name.lower()

        custom_commands.remove_command(command, channel)

        await ctx.send(f"Commande {command} retirée avec succes SeemsGood")

    @commands.command(name="disableautosovip")
    async def disableautosovip(self, ctx: commands.Context):
        """Désactive le shoutout automatique pour les VIP et modérateurs"""
        custom_commands.update_vip_so(ctx.author.channel.name, False)
        await ctx.send('Le so automatique a été désactivé SeemsGood')

    @commands.command(name="enableautosovip")
    async def enableautosovip(self, ctx: commands.Context):
        """Active le shoutout automatique pour les VIP et modérateurs"""
        custom_commands.update_vip_so(ctx.author.channel.name, True)
        await ctx.send('Le so automatique a été activé SeemsGood')

    @commands.command(name="addso")
    async def unban(self, ctx: commands.Context, user: User = None):
        """TODO"""

    @commands.command(name="removeso")
    async def unban(self, ctx: commands.Context, user: User = None):
        """TODO"""

    @commands.command(name="disablebotreplies")
    async def disablebotreplies(self, ctx: commands.Context):
        """Désactive les réponses automatiques aux bots"""
        custom_commands.update_bot_replies(ctx.author.channel.name, False)
        await ctx.send('Les réponses automatiques aux bots ont été désactivées SeemsGood')

    @commands.command(name="enablebotreplies")
    async def enablebotreplies(self, ctx: commands.Context):
        """Active les réponses automatiques aux bots"""
        custom_commands.update_bot_replies(ctx.author.channel.name, True)
        await ctx.send('Les réponses automatiques aux bots ont été activées SeemsGood')


def prepare(bot: commands.Bot):
    bot.add_cog(CustomCommand(bot))
