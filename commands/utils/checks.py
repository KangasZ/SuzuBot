from discord.ext import commands

def is_mod():
    async def pred(ctx):
        #return await check_guild_permissions(ctx, {'manage_guild': True})
        return True
    return commands.check(pred)