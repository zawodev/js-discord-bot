import discord
from discord.ext import commands
from utils.saving_loading_json import load_setting_json

def format_message(message, name):
    return message.replace('{name}', name)


class WelcomeGoodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        settings = load_setting_json('welcome_goodbye_settings')
        channel_name = settings['channel_name']
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            message = format_message(settings['welcome_message'], member.mention)
            await channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        settings = load_setting_json('welcome_goodbye_settings')
        channel_name = settings['channel_name']
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            message = format_message(settings['goodbye_message'], member.mention)
            await channel.send(message)

async def setup(bot):
    await bot.add_cog(WelcomeGoodbye(bot))
