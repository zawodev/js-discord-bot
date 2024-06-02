from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit
from utils.saving_loading_json import load_setting_json, save_setting_json

class FetchData(QWidget):
    def __init__(self):
        super().__init__()

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
        # from discord
        pass
