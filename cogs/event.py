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
            Run('myztroraisy',
                'Quake III Arena',
                'Full Game Nightmare! Any%',
                datetime.timedelta(minutes=35),
                ['Leix34', 'Fight_Like_Hell']),
            Run('danejerus',
                'Fashion Police Squad',
                '100%',
                datetime.timedelta(hours=1, minutes=35),
                ['Kingostone', 'BadOmen']),
            Run('clouder322 ',
                'DUSK',
                'Any% Inbounds Standard',
                datetime.timedelta(minutes=25),
                ['Fight_Like_Hell', 'Leix34']),
            Run('clouder322',
                'Quake',
                'Easy run',
                datetime.timedelta(minutes=20),
                ['n9va', 'Fight_Like_Hell']),
            Run('gycnob vs quarth234',
                'DOOM Eternal TAG1',
                'Any% Restricted',
                datetime.timedelta(minutes=26),
                ['Lickers_', 'Fight_Like_Hell']),
            Run('eold',
                'Black Mesa',
                '0.9 no void',
                datetime.timedelta(hours=1, minutes=35),
                ['Lickers_', 'Leix34']),
            Run('pepethedestructor',
                'Return to Castle Wolfenstein',
                'rtcw any%',
                datetime.timedelta(minutes=45),
                ['Daliakes', 'n0va']),
            Run('Raitro',
                'Shadow Warrior 3',
                'All arenas hardcore',
                datetime.timedelta(hours=1, minutes=35),
                ['Kingostone', 'Fight_Like_Hell']),
            Run('Nerd_Squared',
                'Half-Life: Alyx',
                'Any% no sprin',
                datetime.timedelta(minutes=40),
                ['BadOmen']),
            Run('minifish',
                'Doom 2016',
                '0% Nightmare',
                datetime.timedelta(hours=2, minutes=45),
                ['BadOmen']),
        ]
        self.current_run = 0

    @commands.cooldown(rate=1, per=360, bucket=commands.Bucket.channel)
    @commands.command(aliases=["denfest"])
    async def event(self, ctx: commands.Context):
        """Annonce pour l'événement a venir. Ex: !mdsr"""

        await ctx.send(
            "La deuxieme édition du Denfest arrive le 9 décembre! Au programme: "
            "du Doom-like a toute vitesse et des runs de Souls frame perfect! "
            "Venez nombreux sur https://www.twitch.tv/dentvfr !"
        )

    # @commands.command(name="trailer")
    # async def trailer(self, ctx: commands.Context):
    #     await ctx.send("Le trailer de MDSR '23: https://youtu.be/oG827fmr4t4")

    # @commands.command(name='run', aliases='encours')
    # async def run(self, ctx: commands.Context):
    #     run = self.planning[self.current_run]
    #     await ctx.send(
    #         f'{run.runner} flex sur {run.game} dans la catégorie '
    #         f'{run.category}. Le temps estimé de la run est de '
    #         f"{humanize.precisedelta(run.expected_time, minimum_unit='seconds')}"
    #     )
    
    # @commands.command(name='suivant', aliases=['next'])
    # async def suivant(self, ctx: commands.Context):
    #     self.current_run += 1
    #     run = self.planning[self.current_run]
    #     await ctx.send(
    #         f"La run suivante vient de commencer! C'est au tour de "
    #         f"{run.runner} de flex sur {run.game}"
    #     )
    
    # @commands.command(name='precedent', aliases=['previous', 'prev'])
    # async def precedent(self, ctx: commands.Context):
    #     self.current_run = max(0, self.current_run - 1)
    #     run = self.planning[self.current_run]
    #     await ctx.send(
    #         f"Oups, la run d'avant n'est pas encore finie! "
    #         f"{run.runner} flex sur {run.game}"
    #     )
    
    # @commands.command(name='runs', aliases=['avenir'])
    # async def runs(self, ctx: commands.Context):
    #     runs_restantes = "Les runs à venir: "
    #     for run in self.planning[self.current_run:]:
    #         runs_restantes += str(run) + ', '
    #     await ctx.send(runs_restantes[:-2])
    
    # @commands.command(name='runner')
    # async def runner(self, ctx: commands.Context):
    #     run = self.planning[self.current_run]
    #     await ctx.send(
    #         f"Tu aimes le gameplay? Retrouve {run.runner}"
    #         f" sur twitch.tv/{run.runner}!"
    #     )
    
    # @commands.command(name='caster', aliases=['casters', 'cast'])
    # async def caster(self, ctx: commands.Context):
    #     run = self.planning[self.current_run]
    #     await ctx.send(
    #         f"Tu aimes les casters? Retrouve {run.casters[0]}"
    #         f" sur twitch.tv/{run.casters[0]} et {run.casters[1]} "
    #         f" sur twitch.tv/{run.casters[1]}"
    #     )

    ## ROUTINES ##
    # @routines.routine(minutes=30.0, wait_first=False)
    # async def links(self):
    #     denTV = self.bot.get_channel('dentvfr')
    #     await denTV.send("Vous voulez voir le stream principal en Anglais? C'est par ici: https://www.twitch.tv/moderndoomspeedrunning")
    #     await asyncio.sleep(60 * 30)
    #     await denTV.send("Ce marathon est au profit de l'association 988 Crisis and Suicide Lifeline. !don pour en savoir plus!")
    #     await asyncio.sleep(60 * 30)

    @commands.Cog.event()
    async def event_ready(self):
        self.links.start()

def prepare(bot: commands.Bot):
    logging.warning("Pas d'evenement alors skip")
    bot.add_cog(Event(bot))
