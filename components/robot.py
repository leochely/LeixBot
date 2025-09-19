from twitchio.ext import commands
import logging
import serial

LOGGER: logging.Logger = logging.getLogger("Components.Robot")

class Robot(commands.Component):
    def __init__(self, bot: commands.AutoBot):
        self.bot = bot
        self.port = "/dev/rfcomm0"
        try:
            self.bluetooth = serial.Serial(self.port, 9600)
            LOGGER.info("Bluetooth robot connected")
        except serial.serialutil.SerialException:
            LOGGER.warning("Bluetooth robot not connected")

    @property
    def is_connected(self) -> bool:
        try:
            return self.bluetooth.is_open
        except AttributeError:
            return False

    @commands.command(name="forward")
    async def forward(self, ctx: commands.Context):
        """Envoie l'ordre d'avancer au robot. Ex: !forward"""
        self.bluetooth.flushInput()
        self.bluetooth.write(b"FORWARD")


async def setup(bot: commands.AutoBot):
    robot = Robot(bot)
    if robot.is_connected:
        await bot.add_component(robot)
    else:
        LOGGER.warning("Robot component not loaded, bluetooth not connected")