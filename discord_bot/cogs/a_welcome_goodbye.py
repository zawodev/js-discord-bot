import discord
from discord.ext import commands
from utils.settings import load_setting

def format_message(message, name):
    return message.replace('{name}', name)


class WelcomeGoodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_name = load_setting('CHANNEL_NAME')
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            message = format_message(load_setting('WELCOME_MESSAGE'), member.mention)
            await channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel_name = load_setting('CHANNEL_NAME')
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            message = format_message(load_setting('GOODBYE_MESSAGE'), member.mention)
            await channel.send(message)

async def setup(bot):
    await bot.add_cog(WelcomeGoodbye(bot))
