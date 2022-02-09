from discord.ext import commands
from discord.ext.commands import command
import sys
from utils.config import Config
import discord


class Suzu(commands.AutoShardedBot):
    def __init__(self, dev):
        self._config = Config()
        intents = discord.Intents.all()
        self._token = self._config.get_val('token')
        self._prefix = self._config.get_val('prefix')
        super().__init__(command_prefix=self._prefix, intents=intents)
        self.owner_id = self._config.get_val('owner')
        self.load_extension("commands.test")
        self.load_extension("commands.C9")
        self.load_extension("handlers.rules")
        super().run(self._token, reconnect=True, bot=True)

    async def on_ready(self):
        print("Bot Initialized.")


if __name__ == "__main__":
    print(sys.argv)
    dev = False
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "dev":
            dev = True
    suzu = Suzu(True)