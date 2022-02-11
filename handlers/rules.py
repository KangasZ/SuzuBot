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
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        gid = str(payload.guild_id)
        if gid in self.rules_dict:
            guild_dict = self.rules_dict[gid]
            if str(payload.channel_id) not in guild_dict["listeners"]:
                return
            if str(payload.message_id) == guild_dict["listeners"][str(payload.channel_id)]:
                return
            guild_dict = self.rules_dict[gid]
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
            for k in guild_dict["rules"]:
                if reaction.emoji in guild_dict["rules"][k]["react"]:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    roles = discord.utils.get(guild.roles, id=int(guild_dict["rules"][k]["react"][reaction.emoji]))
                    await member.add_roles(roles)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        gid = str(payload.guild_id)
        if gid in self.rules_dict:
            guild_dict = self.rules_dict[gid]
            if str(payload.channel_id) not in guild_dict["listeners"]:
                return
            if str(payload.message_id) == guild_dict["listeners"][str(payload.channel_id)]:
                return
            guild_dict = self.rules_dict[gid]
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
            for k in guild_dict["rules"]:
                if reaction.emoji in guild_dict["rules"][k]["react"]:
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    roles = discord.utils.get(guild.roles, id=int(guild_dict["rules"][k]["react"][reaction.emoji]))
                    await member.remove_roles(roles)

    @commands.is_owner()
    @commands.command(name='rules', aliases=['Rules', 'RULES'], hidden=True)
    async def rules(self, ctx: discord.ext.commands.Context, *arg):
        #await ctx.channel.send("owner only ovo")
        guild_dict: dict
        if str(ctx.guild.id) not in self.rules_dict:
            self.rules_dict[str(ctx.guild.id)] = {
                "listeners": {},
                "rules": {}
            }
        guild_dict = self.rules_dict[str(ctx.guild.id)]
        rule_dict: dict
        if len(arg) > 1 and arg[1] != "create":
            try:
                rule_dict = guild_dict["rules"][arg[0]]
            except KeyError:
                await ctx.channel.send("Call create on this name.")
                return
            if arg[1] == "post":
                name: str = arg[1]
                guild: discord.Guild = ctx.guild
                channel: discord.TextChannel = ctx.channel
                embed = discord.Embed.from_dict(rule_dict["embed"])
                message: discord.Message = await channel.send(embed=embed)
                # TODO manage reactions
                rule_dict["cid"] = message.channel.id
                rule_dict["mid"] = message.id
                if "react" in rule_dict:
                    guild_dict["listeners"] = {}
                    for k in guild_dict["rules"]:
                        if "react" in guild_dict["rules"][k]:
                            guild_dict["listeners"][str(guild_dict["rules"][k]["cid"])] = str(guild_dict["rules"][k]["mid"])
                    for k in rule_dict["react"]:
                        await message.add_reaction(emoji=k)
                await ctx.message.delete()
            elif arg[1] == "field":
                name = arg[1]
                fields: list = rule_dict["embed"]["fields"]
                fields.append({"inline": False, "name": arg[2], "value": arg[3]})
            elif arg[1] == "clear":
                name = arg[1]
                rule_dict["embed"]["fields"] = []
                rule_dict["embed"].pop("footer", None)
            elif arg[1] == "footer":
                name = arg[1]
                rule_dict["embed"]["footer"] = {"text": arg[2]}
            elif arg[1] == "preview":
                name = arg[1]
                try:
                    embed = discord.Embed.from_dict(rule_dict["embed"])
                    await ctx.channel.send(embed=embed)
                except KeyError:
                    await ctx.channel.send("Something went wrong")
            elif arg[1] == "react":
                name = arg[1]
                if arg[2] == "remove":
                    rule_dict.pop("react", None)
                else:
                    if "react" not in rule_dict:
                        rule_dict["react"] = {}
                    rule_dict["react"][arg[2]] = arg[3]
        elif arg[1] == "create":
            name: str = arg[0]
            title: str = arg[2]
            color = int(arg[3])
            guild_dict["rules"][arg[0]] = {
                "embed": {"title": title, "color": color, "type": "rich", "fields": []}
            }
            await ctx.channel.send(f"Now, type %rules field/footer {name} [args]")
        elif arg[0] == "list":
            pot = ""
            for k in guild_dict["rules"]:
                pot = pot + f"\t{k}\n"
            await ctx.channel.send(f"List for server {ctx.guild.name}\n{pot}")
        elif arg[0] == "dev":
            await ctx.channel.send(f"```json\n{guild_dict}\n```")
        with open("rules.toml", 'w', encoding="utf-8") as json_file:
            toml.dump(self.rules_dict, json_file)
        #print(self.rules_dict[str(ctx.guild.id)])

def setup(bot):
    bot.add_cog(Rules(bot))