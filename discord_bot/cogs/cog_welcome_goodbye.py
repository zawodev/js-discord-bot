import discord
from discord.ext import commands
from utils.saving_loading_json import load_setting_json, save_setting_json

def format_message(message, changes):
    for key, value in changes.items():
        message = message.replace(key, value)
    return message

class WelcomeGoodbye(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        settings = load_setting_json('welcome_goodbye_settings')
        user_data = load_setting_json('user_data')
        channel_name = settings['channel_name']
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            changes = {
                '{user_name}': member.mention,
                '{guild_name}': member.guild.name
            }
            message = format_message(settings['welcome_message'], changes)
            if str(member.id) in user_data:
                user_data[str(member.id)]['is_in_guild'] = True
            else:
                user_data[str(member.id)] = {
                    'is_in_guild': True,
                }
            save_setting_json('user_data', user_data)
            await channel.send(message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        settings = load_setting_json('welcome_goodbye_settings')
        user_data = load_setting_json('user_data')
        channel_name = settings['channel_name']
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            changes = {
                '{user_name}': member.mention,
                '{guild_name}': member.guild.name
            }
            message = format_message(settings['goodbye_message'], changes)
            if str(member.id) in user_data:
                user_data[str(member.id)]['is_in_guild'] = False
            else:
                user_data[str(member.id)] = {
                    'is_in_guild': False,
                }
            save_setting_json('user_data', user_data)
            await channel.send(message)

async def setup(bot):
    await bot.add_cog(WelcomeGoodbye(bot))
