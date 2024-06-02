from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox
from utils.saving_loading_json import load_setting_json, save_setting_json

class FetchData(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        # save button
        self.fetch_button = QPushButton("Fetch Data")
        self.fetch_button.clicked.connect(self.fetch_data)

        # label
        self.discord_guild_id_label = QLabel("Guild ID:")
        self.discord_guild_id_input = QLineEdit()

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.discord_guild_id_label)
        layout.addWidget(self.discord_guild_id_input)
        layout.addWidget(self.fetch_button)
        self.setLayout(layout)

    def fetch_data(self):
        self.bot.loop.create_task(self.collect_data())
        QMessageBox.information(self, "Success", "Data collected successfully.")

    async def collect_data(self):
        messages_data = {}
        channel_data = {}
        print("Collecting data...")

        for guild in self.bot.guilds:
            for member in guild.members:
                messages_data[member.id] = 0
            print(f"Collected data for {guild.name} members.")
            for channel in guild.text_channels:
                channel_data[channel.id] = {
                    "messages_count": 0,
                    "name": channel.name
                }
                async for message in channel.history(limit=None):
                    if message.author.id in messages_data:
                        messages_data[message.author.id] += 1
                    if channel.id in channel_data:
                        channel_data[channel.id]["messages_count"] += 1
            print(f"Collected data for {guild.name} channels.")

        self.modify_users("user_data", messages_data)
        save_setting_json("channel_stats", channel_data)

    def modify_users(self, key, messages_data):
        data = load_setting_json(key)
        for user_id, messages_count in messages_data.items():
            if user_id in data:
                data[str(user_id)]["messages_count"] += messages_count
            else:
                data[str(user_id)]["messages_count"] = messages_count
        save_setting_json(key, data)
