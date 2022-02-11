from discord.ext import commands
import discord
import toml
from commands.utils import checks
import typing
import re

class Rules(commands.Cog, name='Handlers'):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        # todo role listener
        try:
            with open("rules.toml", 'r', encoding="utf-8") as json_file:
                self.rules_dict = toml.load(json_file)
        except:
            with open("rules.toml", 'w', encoding="utf-8") as json_file:
                self.rules_dict = {"version": 1}
                toml.dump(self.rules_dict, json_file)

    @commands.Cog.listener()
    async def on_ready(self):
        #for key in self.rules_dict:
        #    guild_dict = self.rules_dict[key]
        #    channel = self.bot.get_channel(guild_dict["channel"])
        #    message = await channel.fetch_message(guild_dict["message"])
        #    await message.add_reaction(emoji=guild_dict["emoji"])
        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        gid = str(payload.guild_id)
        if gid in self.rules_dict:
            guild_dict = self.rules_dict[gid]
            if "role" not in guild_dict:
                return
            if payload.message_id == guild_dict["message"]:
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
            guild_dict = self.rules_dict[gid]
            if "role" not in guild_dict:
                return
            if payload.message_id == guild_dict["message"]:
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

                if reaction.emoji == guild_dict["emoji"]:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    roles = discord.utils.get(guild.roles, id=guild_dict["role"])
                    await member.remove_roles(roles)

    @commands.is_owner()
    @commands.command(name='rules', aliases=['Rules', 'RULES'], hidden=True)
    async def rules(self, ctx: discord.ext.commands.Context, *arg):
        await ctx.channel.send("owner only ovo")
        guild_dict: dict
        if str(ctx.guild.id) not in self.rules_dict:
            self.rules_dict[str(ctx.guild.id)] = {}
        guild_dict = self.rules_dict[str(ctx.guild.id)]
        if arg[0] == "post":
            name: str = arg[1]
            guild: discord.Guild = ctx.guild
            channel: discord.TextChannel = ctx.channel
            embed = discord.Embed.from_dict(guild_dict[name]["embed"])
            message: discord.Message = await channel.send(embed=embed)
            # TODO manage reactions
            guild_dict[name]["cid"] = message.channel.id
            guild_dict[name]["mid"] = message.id
            await ctx.message.delete()
        elif arg[0] == "create":
            name: str = arg[1]
            title: str = arg[2]
            color = int(arg[3])
            guild_dict[name] = {
                "embed": {"title": title, "color": color, "type": "rich", "fields": []}
            }
            await ctx.channel.send(f"Now, type %rules field/footer {name} [args]")
        elif arg[0] == "field":
            name = arg[1]
            fields: list = guild_dict[name]["embed"]["fields"]
            fields.append({"inline": False, "name": arg[2], "value": arg[3]})
        elif arg[0] == "clear":
            name = arg[1]
            guild_dict[name]["embed"]["fields"] = []
            guild_dict[name]["embed"].pop("footer", None)
        elif arg[0] == "footer":
            name = arg[1]
            guild_dict[name]["embed"]["footer"] = {"text": arg[2]}
        elif arg[0] == "preview":
            name = arg[1]
            try:
                embed = discord.Embed.from_dict(guild_dict[name]["embed"])
                await ctx.channel.send(embed=embed)
            except KeyError:
                await ctx.channel.send("Something went wrong")
        elif arg[0] == "list":
            pass
        elif arg[0] == "dev":
            await ctx.channel.send(f"```json\n{guild_dict}\n```")
        elif arg[0] == "react":
            name = arg[1]
            if arg[2] == "remove":
                guild_dict[name].pop("react", None)
            else:
                if "react" not in guild_dict[name]:
                    guild_dict[name]["react"] = {}
                guild_dict[name]["react"][arg[2]] = arg[3]
        with open("rules.toml", 'w', encoding="utf-8") as json_file:
            toml.dump(self.rules_dict, json_file)
        #print(self.rules_dict[str(ctx.guild.id)])

def setup(bot):
    bot.add_cog(Rules(bot))