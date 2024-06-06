import discord
from discord import app_commands
from discord.ext import commands
import random

from utils.saving_loading_json import load_setting_json, save_setting_json

class MiniGame(commands.Cog):
    def __init__(self, bot):
        self.choices = ["papier", "kamień", "nożyce"]
        self.user_scores = load_setting_json("rock_paper_scissors")
        self.bot = bot

    def check_winner(self, user_choice, bot_choice):
        if user_choice == bot_choice:
            return "Remis!"
        elif (user_choice == "papier" and bot_choice == "kamień") or \
                (user_choice == "kamień" and bot_choice == "nożyce") or \
                (user_choice == "nożyce" and bot_choice == "papier"):
            return "Wygrywasz!"
        else:
            return "Przegrywasz!"

    # funkcja obsługująca grę
    async def play_game(self, interaction, user_choice):
        bot_choice = random.choice(self.choices)
        result = self.check_winner(user_choice, bot_choice)
        user_id = str(interaction.user.id)

        if user_id not in self.user_scores:
            self.user_scores[user_id] = {"wins": 0, "losses": 0, "ties": 0}

        if result == "Wygrywasz!":
            self.user_scores[user_id]["wins"] += 1
        elif result == "Przegrywasz!":
            self.user_scores[user_id]["losses"] += 1
        elif result == "Remis!":
            self.user_scores[user_id]["ties"] += 1

        total_wins = self.user_scores[user_id]["wins"]
        total_losses = self.user_scores[user_id]["losses"]
        total_ties = self.user_scores[user_id]["ties"]

        save_setting_json("rock_paper_scissors", self.user_scores)

        await interaction.response.send_message(
            f"Twój wybór: {user_choice}\n"
            f"Wybór bota: {bot_choice}\n"
            f"Wynik: {result}\n"
            f"Twoje wyniki: {total_wins} wygranych, {total_losses} przegranych, {total_ties} remisów"
         )

    @app_commands.command(name="papier", description="Graj w papier, kamień, nożyce - wybierz papier")
    async def papier(self, interaction: discord.Interaction):
        await self.play_game(interaction, "papier")

    @app_commands.command(name="kamien", description="Graj w papier, kamień, nożyce - wybierz kamień")
    async def kamien(self, interaction: discord.Interaction):
        await self.play_game(interaction, "kamień")

    @app_commands.command(name="nozyce", description="Graj w papier, kamień, nożyce - wybierz nożyce")
    async def nozyce(self, interaction: discord.Interaction):
        await self.play_game(interaction, "nożyce")


async def setup(bot):
    await bot.add_cog(MiniGame(bot))