from discord.ext import commands


class C9(commands.Cog, name='test suite'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='c9')
    async def test(self, ctx, *arg):
        await ctx.message.delete()
        await ctx.channel.send("C9 HOPIUM")
        await ctx.channel.send("C9 HOPIUM")


def setup(bot):
    bot.add_cog(C9(bot))