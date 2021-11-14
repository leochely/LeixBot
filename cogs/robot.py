from twitchio.ext import commands
import logging
import serial

class Robot(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.port="/dev/rfcomm0"
        try:
            self.bluetooth=serial.Serial(self.port, 9600)
            logging.info("Bluetooth robot connected")
        except serial.serialutil.SerialException:
            logging.warning("Bluetooth robot not connected")

    @commands.command(name="forward")
    async def forward(self, ctx: commands.Context):
        self.bluetooth.flushInput()
        self.bluetooth.write(b"FORWARD")

def prepare(bot: commands.Bot):
    bot.add_cog(Robot(bot))
