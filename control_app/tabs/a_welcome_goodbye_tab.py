from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit
from utils.settings import load_setting, save_setting

class WelcomeGoodbyeTab(QWidget):
    def __init__(self):
        super().__init__()

        # channel name
        channel_name_label = QLabel("Channel Name:")
        self.channel_name = QLineEdit()
        self.channel_name.setPlaceholderText("Enter the channel name")
        self.channel_name.setText(load_setting('CHANNEL_NAME'))

        # welcome
        welcome_label = QLabel("Welcome Message:")
        self.welcome_message = QTextEdit()
        self.welcome_message.setPlaceholderText("Enter the welcome message")
        self.welcome_message.setPlainText(load_setting('WELCOME_MESSAGE'))

        # farewell
        goodbye_label = QLabel("Goodbye Message:")
        self.goodbye_message = QTextEdit()
        self.goodbye_message.setPlaceholderText("Enter the goodbye message")
        self.goodbye_message.setPlainText(load_setting('GOODBYE_MESSAGE'))

        # save button
        save_button = QPushButton("Save Messages")
        save_button.clicked.connect(self.save_welcome_farewell_messages)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(channel_name_label)
        layout.addWidget(self.channel_name)
        layout.addWidget(welcome_label)
        layout.addWidget(self.welcome_message)
        layout.addWidget(goodbye_label)
        layout.addWidget(self.goodbye_message)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_welcome_farewell_messages(self):
        channel_name = self.channel_name.text()
        welcome_msg = self.welcome_message.toPlainText()
        goodbye_msg = self.goodbye_message.toPlainText()

        save_setting('CHANNEL_NAME', channel_name)
        save_setting('WELCOME_MESSAGE', welcome_msg)
        save_setting('GOODBYE_MESSAGE', goodbye_msg)

        print(f"Saved Channel Name: {channel_name}")
        print(f"Saved Welcome Message: {welcome_msg}")
        print(f"Saved Goodbye Message: {goodbye_msg}")

