from discord.ext import commands
import discord


class Rules(commands.Cog, name='Handlers'):
    def __init__(self, bot):
        self.bot = bot
        self.rules_message = {940633019843231775: None}
        self.rules_channel = {771823946651795526: None}

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(771823946651795526)
        message = await channel.fetch_message(940633019843231775)
        await message.add_reaction(emoji='✅')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = self.bot.get_guild(payload.guild_id)
        # Put the following Line
        member = guild.get_member(payload.user_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

        # only work if it is the client
        if payload.user_id == self.bot.user.id:
            return

        if payload.message_id == 940633019843231775 and reaction.emoji == '✅':
            roles = discord.utils.get(guild.roles, name='Yerr')
            await member.add_roles(roles)
            await reaction.remove(payload.member)

    @commands.is_owner()
    @commands.command(name='rules', aliases=['Rules', 'RULES'])
    async def rules(self, ctx, *arg):
        await ctx.channel.send("owner only ovo")

def setup(bot):
    bot.add_cog(Rules(bot))