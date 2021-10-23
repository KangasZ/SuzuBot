from discord.ext import commands
from discord.ext.commands import command

from utils.config import Config
import discord


class Suzu(commands.AutoShardedBot):
    def __init__(self):
        self._config = Config()
        intents = discord.Intents.default()
        self._token = self._config.get_val('token')
        self._prefix = self._config.get_val('prefix')
        super().__init__(command_prefix='%')

        '''@command(name='test')
        async def test(ctx, arg):
            ctx.send("wow this test worked peepowut")

        self.add_command(test)'''
        self.load_extension("commands.test")

        super().run(self._token, reconnect=True, bot=True)

    async def on_ready(self):
        print("hi")



    '''async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        if message.content.startswith(self._prefix):
            await message.channel.send(message.content[1::])'''

suzu = Suzu()