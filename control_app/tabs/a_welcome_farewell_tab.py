from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit

class WelcomeFarewellTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # welcome
        welcome_label = QLabel("Welcome Message:")
        self.welcome_message = QTextEdit()

        # farewell
        farewell_label = QLabel("Farewell Message:")
        self.farewell_message = QTextEdit()

        # save button
        save_button = QPushButton("Save Messages")
        save_button.clicked.connect(self.save_welcome_farewell_messages)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(welcome_label)
        layout.addWidget(self.welcome_message)
        layout.addWidget(farewell_label)
        layout.addWidget(self.farewell_message)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_welcome_farewell_messages(self):
        welcome_msg = self.welcome_message.toPlainText()
        farewell_msg = self.farewell_message.toPlainText()

        with open('settings.txt', 'w') as file:
            file.write(f'WELCOME_MESSAGE={welcome_msg}\n')
            file.write(f'FAREWELL_MESSAGE={farewell_msg}\n')

        print(f"Saved Welcome Message: {welcome_msg}")
        print(f"Saved Farewell Message: {farewell_msg}")

