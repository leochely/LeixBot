from playsound import playsound
from twitchio.ext import commands


class Sound(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.cooldown(1, 60, commands.Bucket.channel)
    @commands.command(name="dontlookback", aliases=['dlb', 'guilty'])
    async def dontlookback(self, ctx: commands.Context):
        playsound('sounds/dontlookback.wav', False)
        await ctx.send("Kreygasm")


def prepare(bot: commands.Bot):
    bot.add_cog(Sound(bot))
