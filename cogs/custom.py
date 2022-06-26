import datetime
import logging
import os

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


def prepare(bot: commands.Bot):
    bot.add_cog(CustomCommand(bot))
