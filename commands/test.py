from discord.ext import commands


class Test(commands.Cog, name='test suite'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx, *arg):
        await ctx.channel.send("wow this test worked peepowut")

def setup(bot):
    bot.add_cog(Test(bot))