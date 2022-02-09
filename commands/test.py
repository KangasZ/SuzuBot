import discord
from discord.ext import commands


class Test(commands.Cog, name='test suite'):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name='test', hidden=True)
    async def test(self, ctx:commands.Context, *arg):
        embed = discord.Embed(title="Tranquility Rules",
                              type="rich",
                              color=0xa300a3)
        #embed.set_author(name="Gurus")
        embed.add_field(name="1", value="No silly drama", inline=False)
        embed.add_field(name="2", value="Be nice", inline=False)
        embed.add_field(name="3", value="Have fun", inline=False)
        embed.add_field(name="Questions, issues, concerns?", value=f"Message <@{self.bot.owner_id}> or <@111668761810964480>", inline=False)
        embed.set_footer(text="React below to access the server")
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Test(bot))