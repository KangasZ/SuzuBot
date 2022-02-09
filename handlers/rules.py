from discord.ext import commands
import discord
import toml
from commands.utils import checks
import typing

class Rules(commands.Cog, name='Handlers'):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        with open("rules.toml", 'r', encoding="utf-8") as json_file:
            self.rules_dict = toml.load(json_file)

    @commands.Cog.listener()
    async def on_ready(self):
        for key in self.rules_dict:
            guild_dict = self.rules_dict[key]
            channel = self.bot.get_channel(guild_dict["channel"])
            message = await channel.fetch_message(guild_dict["message"])
            await message.add_reaction(emoji=guild_dict["emoji"])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        gid = str(payload.guild_id)
        if gid in self.rules_dict:
            if payload.message_id == self.rules_dict[gid]["message"]:
                guild_dict = self.rules_dict[gid]
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                if reaction.emoji == guild_dict["emoji"]:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    roles = discord.utils.get(guild.roles, id=guild_dict["role"])
                    await member.add_roles(roles)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        gid = str(payload.guild_id)
        if gid in self.rules_dict:
            if payload.message_id == self.rules_dict[gid]["message"]:
                guild_dict = self.rules_dict[gid]
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

                if reaction.emoji == guild_dict["emoji"]:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    roles = discord.utils.get(guild.roles, id=guild_dict["role"])
                    await member.remove_roles(roles)

    @commands.is_owner()
    @checks.is_mod()
    @commands.command(name='rules', aliases=['Rules', 'RULES'], hidden=True)
    async def rules(self, ctx: discord.ext.commands.Context, *arg):
        await ctx.channel.send("owner only ovo")
        if len(arg) == 3:
            await ctx.channel.send(f"Sending Rules to ID {arg[0]}")
            channel_id = int(arg[0])
            role_id = int(arg[1])
            emoji = arg[2]
            guild: discord.Guild = ctx.guild
            channel: discord.TextChannel = discord.utils.get(guild.text_channels, id=channel_id)
            embed = discord.Embed(title="Tranquility Rules",
                                  type="rich",
                                  color=0xa300a3)
            # embed.set_author(name="Gurus")
            embed.add_field(name="1", value="No silly drama", inline=False)
            embed.add_field(name="2", value="Be nice", inline=False)
            embed.add_field(name="3", value="Have fun", inline=False)
            embed.add_field(name="Questions, issues, concerns?",
                            value=f"Message <@{self.bot.owner_id}> or <@111668761810964480>", inline=False)
            embed.set_footer(text="React below to access the server")
            message: discord.Message = await channel.send(embed=embed)
            await message.add_reaction(emoji=emoji)
            self.rules_dict[str(message.guild.id)] = {
                "channel": message.channel.id,
                "message": message.id,
                "emoji": emoji,
                "role": role_id
            }
            with open("rules.toml", 'w', encoding="utf-8") as json_file:
                toml.dump(self.rules_dict, json_file)


def setup(bot):
    bot.add_cog(Rules(bot))