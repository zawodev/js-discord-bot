import discord
from discord import app_commands
from discord.ext import commands
import random

from utils.saving_loading_json import load_setting_json, save_setting_json

class MiniGame(commands.Cog):
    def __init__(self, bot):
        """
        Initializes the MiniGame cog with game choices and loads user scores from JSON.
        """
        self.choices = ["papier", "kamień", "nożyce"]
        self.user_scores = load_setting_json("rock_paper_scissors")
        self.bot = bot

    def check_winner(self, user_choice, bot_choice):
        """
        Determines the winner of the game based on the choices made by the user and the bot.
        """
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
        """
        Plays a game of rock-paper-scissors, updates scores, and sends the result to the user.
        """
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
        """
        Command to play the game choosing 'papier'.
        """
        await self.play_game(interaction, "papier")

    @app_commands.command(name="kamien", description="Graj w papier, kamień, nożyce - wybierz kamień")
    async def kamien(self, interaction: discord.Interaction):
        """
        Command to play the game choosing 'kamien'.
        """
        await self.play_game(interaction, "kamień")

    @app_commands.command(name="nozyce", description="Graj w papier, kamień, nożyce - wybierz nożyce")
    async def nozyce(self, interaction: discord.Interaction):
        """
        Command to play the game choosing 'nozyce'.
        """
        await self.play_game(interaction, "nożyce")


async def setup(bot):
    """
    Standard asynchronous setup function to add this cog to a bot instance.
    """
    await bot.add_cog(MiniGame(bot))
