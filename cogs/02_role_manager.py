import discord
from discord import app_commands
from discord.ext import commands

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    @app_commands.command(name="add_role", description="Add a role to a user")
    @app_commands.describe(role="Role to add", member="Member to add the role to")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member = None):
        member = member or interaction.user
        await member.add_roles(role)
        await interaction.response.send_message(f'Role {role.name} added to {member.mention}', ephemeral=True)

    @app_commands.command(name="remove_role", description="Remove a role from a user")
    @app_commands.describe(role="Role to remove", member="Member to remove the role from")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def remove_role(self, interaction: discord.Interaction, role: discord.Role, member: discord.Member = None):
        member = member or interaction.user
        await member.remove_roles(role)
        await interaction.response.send_message(f'Role {role.name} removed from {member.mention}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(RoleManagement(bot))
