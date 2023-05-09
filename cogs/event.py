import asyncio
import datetime
import logging
import os

import humanize
from twitchio import User
from twitchio.ext import commands

# Sets humanize to French language
humanize.i18n.activate("fr_FR")


class Run():
    def __init__(self, runner, game, category, expected_time, casters):
        self.runner = runner
        self.game = game
        self.category = category
        self.expected_time = expected_time
        self.casters = casters

    def __str__(self):
        return f'{self.runner} sur {self.game} (catégorie {self.category}) en {self.expected_time}'


class Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.planning = [
            Run('potdechoucroute',
                'Doom Eternal',
                'Reclaimden et World Spear ML',
                datetime.timedelta(hours=1),
                ['Leix34', 'payoyo5150']),
            Run('KalderinoFeross',
                'DOOM Eternal',
                'Exuden et Mars Den Core',
                datetime.timedelta(hours=1),
                ['Leix34', 'payoyo5150']),
            Run('Haurkrix',
                'Sekiro: Shadows Die Twice',
                'Any% Shura Résurrection Mod',
                datetime.timedelta(hours=1),
                ['OkamiKaz26', 'Lickers__']),
            Run('Fight_Like_Hell',
                'UILTRAKILL',
                'Full Game P-Rank Violent',
                datetime.timedelta(hours=1),
                ['potdechoucroute', 'kiojin999']),
            Run('Kali_Tay',
                'Elden Ring',
                'Malenia%',
                datetime.timedelta(hours=1),
                ['Lickers__', 'KalderinoFeross']),
        ]
        self.current_run = 0

    @commands.cooldown(rate=1, per=360, bucket=commands.Bucket.channel)
    @commands.command(name="mdsr")
    async def mdsr(self, ctx: commands.Context):
        """Annonce pour MDSR 2023. Ex: !mdsr"""

        await ctx.send(
            "MDSR 2023 est un événement caritatif de speedrun au profit "
            "l'association 988 Lifeline. Le marathon démarre le 20 Mai a 17h et "
            "se termine dans la nuit du 21 au 22. Au programme: du Doom classique "
            "et moderne, Ultrakill, DUSK et plein d'autres Doom like!"
        )
        await ctx.send(
            "Venez nous rejoindre sur le restream francais "
            "https://www.twitch.tv/dentvfr ou sur https://www.twitch.tv/moderndoomspeedrunning "
            "pour le cast en anglais."
        )

        @commands.command(name="trailer")
        async def trailer(self, ctx: commands.Context):
            await ctx.send("Le trailer de MDSR '23: https://youtu.be/oG827fmr4t4")

        # @commands.command(name='run', aliases='encours')
        # async def run(self, ctx: commands.Context):
        #     run = self.planning[self.current_run]
        #     await ctx.send(
        #         f'{run.runner} flex sur {run.game} dans la catégorie '
        #         f'{run.category}. Le temps estimé de la run est de '
        #         f"{humanize.precisedelta(run.expected_time, minimum_unit='seconds')}"
        #     )
        #
        # @commands.command(name='suivant', aliases=['next'])
        # async def suivant(self, ctx: commands.Context):
        #     self.current_run += 1
        #     run = self.planning[self.current_run]
        #     await ctx.send(
        #         f"La run suivante vient de commencer! C'est au tour de "
        #         f"{run.runner} de flex sur {run.game}"
        #     )
        #
        # @commands.command(name='precedent', aliases=['previous', 'prev'])
        # async def precedent(self, ctx: commands.Context):
        #     self.current_run = max(0, self.current_run - 1)
        #     run = self.planning[self.current_run]
        #     await ctx.send(
        #         f"Oups, la run d'avant n'est pas encore finie! "
        #         f"{run.runner} flex sur {run.game}"
        #     )
        #
        # @commands.command(name='runs', aliases=['avenir'])
        # async def runs(self, ctx: commands.Context):
        #     runs_restantes = "Les runs à venir: "
        #     for run in self.planning[self.current_run:]:
        #         runs_restantes += str(run) + ', '
        #     await ctx.send(runs_restantes[:-2])
        #
        # @commands.command(name='runner')
        # async def runner(self, ctx: commands.Context):
        #     run = self.planning[self.current_run]
        #     await ctx.send(
        #         f"Tu aimes le gameplay? Retrouve {run.runner}"
        #         f" sur twitch.tv/{run.runner}!"
        #     )
        #
        # @commands.command(name='caster', aliases=['casters', 'cast'])
        # async def caster(self, ctx: commands.Context):
        #     run = self.planning[self.current_run]
        #     await ctx.send(
        #         f"Tu aimes les casters? Retrouve {run.casters[0]}"
        #         f" sur twitch.tv/{run.casters[0]} et {run.casters[1]} "
        #         f" sur twitch.tv/{run.casters[1]}"
        #     )


def prepare(bot: commands.Bot):
    # logging.warning("Pas d'evenement alors skip")
    bot.add_cog(Event(bot))
