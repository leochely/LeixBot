import asyncio
import datetime
import logging

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
            Run('n0va',
                'Doom Eternal',
                'Any% Restricted',
                datetime.timedelta(hours=1, minutes=15),
                ['kalderinofeross', 'payoyo']),
            Run('potdechoucroute',
                'Ultrakill',
                'Any%',
                datetime.timedelta(minutes=20),
                ['Fight_Like_Hell', 'Leix']),
            Run('KEMIST_C10H15N',
                'Elden Ring',
                'Any% Gltichless',
                datetime.timedelta(hours=1, minutes=20),
                ['Shiyatsu', 'Lickers']),
            Run('Fight_Like_Hell',
                'Dusk',
                'Any%',
                datetime.timedelta(minutes=25),
                ['potdechoucroute', 'kiojin999']),
            Run('Haurkrix',
                'Sekiro',
                'LoR mod',
                datetime.timedelta(hours=1, minutes=45),
                ['Lickers_', 'Oka']),
            Run('kiojin999 vs Fight_Like_Hell',
                'Roboquest',
                'Race',
                datetime.timedelta(minutes=30),
                ['kiojin999', 'Fight_Like_Hell']),
            Run('Zenoxyde',
                'Dark Souls 3',
                'Armes discutables',
                datetime.timedelta(hours=2, minutes=45),
                ['kalderinofeross', 'SmallPinkPanda']),
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

    @commands.command(name="trailer")
    async def trailer(self, ctx: commands.Context):
        await ctx.send("Le trailer du Denfest: https://youtu.be/q49eZNtYW80?si=e_-42RroS1dx8ZgU")

    @commands.command(name='run', aliases='encours')
    async def run(self, ctx: commands.Context):
        run = self.planning[self.current_run]
        await ctx.send(
            f'{run.runner} flex sur {run.game} dans la catégorie '
            f'{run.category}. Le temps estimé de la run est de '
            f"{humanize.precisedelta(run.expected_time, minimum_unit='seconds')}"
        )
    
    @commands.command(name='suivant', aliases=['next'])
    async def suivant(self, ctx: commands.Context):
        self.current_run += 1
        run = self.planning[self.current_run]
        await ctx.send(
            f"La run suivante vient de commencer! C'est au tour de "
            f"{run.runner} de flex sur {run.game}"
        )
    
    @commands.command(name='precedent', aliases=['previous', 'prev'])
    async def precedent(self, ctx: commands.Context):
        self.current_run = max(0, self.current_run - 1)
        run = self.planning[self.current_run]
        await ctx.send(
            f"Oups, la run d'avant n'est pas encore finie! "
            f"{run.runner} flex sur {run.game}"
        )
    
    @commands.command(name='runs', aliases=['avenir'])
    async def runs(self, ctx: commands.Context):
        runs_restantes = "Les runs à venir: "
        for run in self.planning[self.current_run:]:
            runs_restantes += str(run) + ', '
        await ctx.send(runs_restantes[:-2]) # Retire la derniere virgule
    
    @commands.command(name='runner')
    async def runner(self, ctx: commands.Context):
        run = self.planning[self.current_run]
        await ctx.send(
            f"Tu aimes le gameplay? Retrouve {run.runner}"
            f" sur twitch.tv/{run.runner}!"
        )
    
    @commands.command(name='caster', aliases=['casters', 'cast'])
    async def caster(self, ctx: commands.Context):
        run = self.planning[self.current_run]
        await ctx.send(
            f"Tu aimes les casters? Retrouve {run.casters[0]}"
            f" sur twitch.tv/{run.casters[0]} et {run.casters[1]} "
            f" sur twitch.tv/{run.casters[1]}"
        )

    ## ROUTINES ##
    @routines.routine(minutes=30.0, wait_first=False)
    async def giveaway(self):
        denTV = self.bot.get_channel('dentvfr')
        await denTV.send("N'hesitez pas de follow! Les followers sont automatiquement inscrits au giveaway! A gagner: des cles pour Mortal Kombat X, B4B et Mad Max!")
        await asyncio.sleep(60 * 60)

    @commands.Cog.event()
    async def event_ready(self):
        self.giveaway.start()

def prepare(bot: commands.Bot):
    logging.warning("Pas d'evenement alors skip")
    # bot.add_cog(Event(bot))
