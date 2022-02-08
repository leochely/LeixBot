import asyncio
import datetime
import logging
import os

import humanize
from twitchio import User
from twitchio.ext import commands, routines

# Sets humanize to French language
humanize.i18n.activate("fr_FR")


class MDSR(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ## Routine ##
    @routines.routine(minutes=30, wait_first=False)
    async def reminders(self):
        channel = self.bot.get_channel(os.environ['CHANNEL'])
        await channel.send("Vous pouvez faire un don pour l'association Save The Children ici:")
        await asyncio.sleep(60 * 30)
        await channel.send("MDSR '22 est un événement caritatif de speedrun des jeux "
                           "Doom modernes et autres Doom-like au profit de l'association "
                           "Save The Children! Le marathon a lieu de 17h a 6h du matin "
                           "samedi et dimanche, retrouvez le planning ici: "
                           "https://oengus.io/en-GB/marathon/mdsrspring/schedule")
        await asyncio.sleep(60 * 30)

    @commands.command(name="don")
    async def don(self, ctx: commands.Context):
        await ctx.send("Vous pouvez faire un don pour l'association Save The Children ici:")

    @commands.command(name="mdsr")
    async def mdsr(self, ctx: commands.Context):
        await ctx.send("MDSR '22 est un événement caritatif de speedrun des jeux "
                       "Doom modernes et autres Doom-like au profit de l'association "
                       "Save The Children! Le marathon a lieu de 17h a 6h du matin "
                       "samedi et dimanche, retrouvez le planning ici: "
                       "https://oengus.io/en-GB/marathon/mdsrspring/schedule")


def prepare(bot: commands.Bot):
    bot.add_cog(MDSR(bot))
