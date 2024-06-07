from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox
from utils.saving_loading_json import load_setting_json, save_setting_json

class SettingsTab(QWidget):
    """
    A QWidget subclass that provides a settings interface for the bot.

    :param bot: The bot instance to interact with the bot's functionalities.
    """

    def __init__(self, bot):
        """
        Initializes the SettingsTab widget.

        :param bot: The bot instance to interact with the bot's functionalities.
        """
        super().__init__()
        self.bot = bot
        self.settings_cog = bot.get_cog("Settings")
        self.fetch_cog = bot.get_cog("FetchData")

        # labels
        self.title_label = QLabel("Settings: ")
        self.title_label.setStyleSheet("position: absolute; bottom: 10px;")
        self.discord_guild_id_label = QLabel("Guild ID:")
        self.discord_guild_id_input = QLineEdit()

        # discord api key - jak zrobić żeby nie było widać hasła?
        self.discord_api_key_label = QLabel("Discord API key:")
        self.discord_api_key_input = QLineEdit()
        self.discord_api_key_input.setEchoMode(QLineEdit.Password)

        # youtube api key
        self.youtube_api_key_label = QLabel("Youtube API key:")
        self.youtube_api_key_input = QLineEdit()
        self.youtube_api_key_input.setEchoMode(QLineEdit.Password)

        self.bot_start_label = QLabel("Bot Start Message:")
        self.bot_start_message = QTextEdit()
        self.bot_start_message.setPlaceholderText("Enter the Bot Start Message")

        self.bot_logs_label = QLabel("Bot logs channel:")
        self.bot_logs_input = QLineEdit()

        # save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)

        self.fetch_button = QPushButton("Fetch Data")
        self.fetch_button.clicked.connect(self.fetch_data)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.discord_guild_id_label)
        layout.addWidget(self.discord_guild_id_input)
        layout.addWidget(self.discord_api_key_label)
        layout.addWidget(self.discord_api_key_input)
        layout.addWidget(self.youtube_api_key_label)
        layout.addWidget(self.youtube_api_key_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.fetch_button)
        layout.addWidget(self.bot_start_label)
        layout.addWidget(self.bot_start_message)
        layout.addWidget(self.bot_logs_label)
        layout.addWidget(self.bot_logs_input)

        self.load_settings()

        # self.fetch_data()
        self.setLayout(layout)

    def save_settings(self):
        """
        Saves the current settings to a JSON file and shows a confirmation message.
        """
        save_setting_json("app_settings", {
            "discord_guild_id": self.discord_guild_id_input.text(),
            "discord_api_key": self.discord_api_key_input.text(),
            "youtube_api_key": self.youtube_api_key_input.text(),
            "bot_start_message": self.bot_start_message.toPlainText(),
            "bot_logs_channel": self.bot_logs_input.text()
        })
        QMessageBox.information(self, "Success", "Settings saved successfully.")

    def load_settings(self):
        """
        Loads settings from a JSON file and populates the input fields with the loaded values.
        """
        settings = load_setting_json("app_settings")
        self.discord_guild_id_input.setText(settings.get("discord_guild_id", ""))
        self.discord_api_key_input.setText(settings.get("discord_api_key", ""))
        self.youtube_api_key_input.setText(settings.get("youtube_api_key", ""))
        self.bot_start_message.setText(settings.get("bot_start_message", ""))
        self.bot_logs_input.setText(settings.get("bot_logs_channel", ""))

    def fetch_data(self):
        """
        Starts the data fetching process and shows a confirmation message.

        If an error occurs, prints the error message.
        """
        try:
            self.bot.loop.create_task(self.fetch_cog.collect_data())
            QMessageBox.information(self, "Success", "Data started downloading. This may take a while.")
        except Exception as e:
            print(f"Failed to collect data: {e}")
