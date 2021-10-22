from playsound import playsound
from twitchio.ext import commands


class Sound(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.Bucket.channel)
    @commands.command(name="testson")
    async def testson(self, ctx: commands.Context):
        playsound('sounds/test.wav', False)
        await ctx.send("Bien ma sonnette? Kappa")


def prepare(bot: commands.Bot):
    bot.add_cog(Sound(bot))
