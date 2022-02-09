from discord.ext import commands


class C9(commands.Cog, name='Hopium'):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.command(name='C9', aliases=['c9'], hidden=True)
    async def test(self, ctx: commands.Context, *arg):
        #await ctx.message.delete()
        if len(arg) != 0:
            if arg[0].lower() == "perkz":
                await ctx.channel.send("PERKZ WHAT ARE YOU DOING")
            if arg[0].lower() == "win":
                await ctx.channel.send("ERROR: C9 WIN NOT FOUND")
            if arg[0].lower() == "worlds":
                await ctx.channel.send("SELL YOUR BOTLANE\nPERKZ WAS A WASTE\nRETHINK YOUR LIVES\nCANT EVEN GET OUT OF SEMIS\nGO BACK TO ACADEMY\nFIRST CLASS SEATS BACK TO NA")
            if arg[0].lower() == "clown":
                await ctx.channel.send("Clown9 Strikes Again")
        else:
            await ctx.channel.send("C9 HOPIUM")


def setup(bot):
    bot.add_cog(C9(bot))