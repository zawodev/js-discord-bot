import discord
from discord.ext import commands


def load_and_format_message(key, name):
    # load from file
    with open('messages.txt', 'r') as file:
        lines = file.readlines()

    messages = {}
    for line in lines:
        k, value = line.strip().split('=', 1)
        messages[k] = value

    message = messages.get(key, f'Message with key "{key}" not found')
    formatted_message = message.replace('{name}', name)

    return formatted_message


class WelcomeGoodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            message = load_and_format_message('WELCOME_MESSAGE', member.mention)
            await channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            await channel.send(f'Goodbye, {member.mention}. We will miss you!')

async def setup(bot):
    await bot.add_cog(WelcomeGoodbye(bot))
