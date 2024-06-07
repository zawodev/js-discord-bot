from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox
from utils.saving_loading_json import load_setting_json, save_setting_json

class WelcomeGoodbyeTab(QWidget):
    """
    A QWidget subclass that provides an interface for setting welcome and goodbye messages.
    """

    def __init__(self):
        """
        Initializes the WelcomeGoodbyeTab widget.
        """
        super().__init__()

        # Channel name
        channel_name_label = QLabel("Channel Name:")
        self.channel_name = QLineEdit()
        self.channel_name.setPlaceholderText("Enter the channel name")

        # Welcome message
        welcome_label = QLabel("Welcome Message: {guild_name} {user_mention}")
        self.welcome_message = QTextEdit()
        self.welcome_message.setPlaceholderText("Enter the welcome message")

        # Goodbye message
        goodbye_label = QLabel("Goodbye Message:")
        self.goodbye_message = QTextEdit()
        self.goodbye_message.setPlaceholderText("Enter the goodbye message")

        # Load initial settings
        self.load_settings()

        # Save button
        save_button = QPushButton("Save Messages")
        save_button.clicked.connect(self.save_welcome_farewell_messages)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(channel_name_label)
        layout.addWidget(self.channel_name)
        layout.addWidget(welcome_label)
        layout.addWidget(self.welcome_message)
        layout.addWidget(goodbye_label)
        layout.addWidget(self.goodbye_message)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_settings(self):
        """
        Loads the settings from a JSON file and updates the fields.

        :raises Exception: If there is an error loading the settings.
        """
        try:
            settings = load_setting_json('welcome_goodbye_settings')
            self.channel_name.setText(settings['channel_name'])
            self.welcome_message.setPlainText(settings['welcome_message'])
            self.goodbye_message.setPlainText(settings['goodbye_message'])
        except Exception as e:
            print(f'Failed to load settings: {e}')

    def save_welcome_farewell_messages(self):
        """
        Saves the current welcome and goodbye messages to a JSON file and shows a success message.
        """
        channel_name = self.channel_name.text()
        welcome_msg = self.welcome_message.toPlainText()
        goodbye_msg = self.goodbye_message.toPlainText()

        save_setting_json('welcome_goodbye_settings', {
            'channel_name': channel_name,
            'welcome_message': welcome_msg,
            'goodbye_message': goodbye_msg
        })
        QMessageBox.information(self, "Success", "Welcome and Goodbye messages saved successfully!")
