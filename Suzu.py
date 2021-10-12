from discord.ext import commands
from utils.config import Config
import discord

class Suzu(discord.Client):
    def __init__(self):
        self._config = Config()
        intents = discord.Intents.default()
        self._token = self._config.get_val('token')
        self._prefix = self._config.get_val('prefix')
        super().__init__()
        super().run(self._token, reconnect=True, bot=True)

    async def on_ready(self):
        print("hi")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content.startswith(self._prefix):
            await message.channel.send(message.content[::1])

suzu = Suzu()