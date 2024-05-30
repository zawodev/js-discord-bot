import discord
from discord.ext import commands
from discord import app_commands

class ChatModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bad_words = ["badword1", "badword2"]
        self.tree = bot.tree

    @commands.Cog.listener()
    async def on_message(self, message):
        if any(bad_word in message.content for bad_word in self.bad_words):
            await message.delete()
            await message.channel.send(f'{message.author.mention}, your message was deleted due to inappropriate content.')

    @app_commands.command(name="mute", description="Mute a user")
    @app_commands.describe(member="Member to mute", reason="Reason for muting")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        mute_role = discord.utils.get(interaction.guild.roles, name='Muted')
        await member.add_roles(mute_role)
        await interaction.response.send_message(f'{member.mention} has been muted. Reason: {reason}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(ChatModeration(bot))
