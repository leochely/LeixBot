import asyncio
import datetime
import logging
import os

import humanize
from twitchio import User
from twitchio.ext import commands, routines

# Sets humanize to French language
humanize.i18n.activate("fr_FR")


class Run():
    def __init__(self, runner, game, category, expected_time):
        self.runner = runner
        self.game = game
        self.category = category
        self.expected_time = expected_time


class MDSR(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.planning = [
            Run('danejerus',
                'DOOM (2016)',
                '100% (Classic) (Crowd Controlled)',
                datetime.timedelta(hours=3)),
            Run('kald',
                'Doom Eternal',
                'Any% restricted classic',
                datetime.timedelta(hours=1, minutes=25)),
            Run('the_kovic',
                'Half-Life Opposing Force',
                'WON Scriptless',
                datetime.timedelta(minutes=30)),
            Run('Scrupy_pup',
                'The Ultimate Doom [Unity Port]',
                'Any%',
                datetime.timedelta(minutes=32)),
            Run('Cindorian',
                'Bright Memory Infinite',
                'Unrestricted Any%',
                datetime.timedelta(minutes=22)),
            Run('ThatGuyBlain',
                'Brutal Doom Episode 1',
                'Power Fantasy Max',
                datetime.timedelta(minutes=35)),
            Run('therealpaisano',
                'DOOM 2016, Eternal',
                'Any%',
                datetime.timedelta(hours=1, minutes=30)),
            Run('--David--',
                'Doom VFR',
                'Any% Classic',
                datetime.timedelta(minutes=15)),
            Run('teddyras',
                'Memoirs of Magic',
                'Any%',
                datetime.timedelta(hours=1, minutes=40)),
            Run('raitro_',
                'Doom Eternal The Ancient Gods Part 2',
                '100% Nightmare ACE',
                datetime.timedelta(minutes=35)),
        ]
        self.current_run = 0

    @commands.command(name="don")
    async def don(self, ctx: commands.Context):
        await ctx.send("Vous pouvez faire un don pour le fond dédié aux enfants victimes "
                       "de la guerre en Ukraine par l'association Save The Children ici: "
                       "https://mdsr.info/donate")

    @commands.command(name="mdsr")
    async def mdsr(self, ctx: commands.Context):
        await ctx.send("MDSR '22 est un événement caritatif de speedrun des jeux "
                       "Doom modernes et autres Doom-like au profit de l'association "
                       "Save The Children! Le marathon dure 2 x 12h a partir de samedi 17h, "
                       "retrouvez le planning ici: https://oengus.io/en-GB/marathon/mdsrspring/schedule")

    @commands.command(name="english")
    async def english(self, ctx: commands.Context):
        await ctx.send("To watch the marathon in English, the main stream is on the MDSR channel: "
                       "https://www.twitch.tv/moderndoomspeedrunning")

    @commands.command(name="run")
    async def run(self, ctx: commands.Context):
        run = self.planning[self.current_run]
        await ctx.send(
            f'{run.runner} speedrun {run.game} dans la catégorie '
            f'{run.category}. Le temps estimé de la run est de '
            f"{humanize.precisedelta(run.expected_time, minimum_unit='seconds')}"
        )

    @commands.command(name="suivant", aliases=['next'])
    async def suivant(self, ctx: commands.Context):
        self.current_run += 1
        run = self.planning[self.current_run]
        await ctx.send(
            f"La run suivante vient de commencer! C'est au tour de "
            f"{run.runner} de speedrun {run.game}"
        )

    @commands.command(name="precedent", aliases=['previous', 'prev'])
    async def precedent(self, ctx: commands.Context):
        self.current_run = max(0, self.current_run - 1)
        run = self.planning[self.current_run]
        await ctx.send(
            f"Oups, la run d'avant n'est pas encore finie! "
            f"{run.runner} speedrun {run.game}"
        )


def prepare(bot: commands.Bot):
    logging.warning("Pas de MDSR alors skip")
    # bot.add_cog(MDSR(bot))
