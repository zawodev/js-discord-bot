import discord
from discord.ext import commands
from discord import app_commands

class UserModerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    async def fetch_users(self):
        guild = self.bot.guilds[0]
        if guild:
            users = {}
            for member in guild.members:
                users[member.id] = {
                    'name': member.name,
                    'avatar_url': str(member.avatar.url if member.avatar else "")
                }
            return users
        return None

async def setup(bot):
    await bot.add_cog(UserModerator(bot))
