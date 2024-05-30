from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class ChatModeratorTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # moderation
        moderation_label = QLabel("Chat Moderation:")

        # buttons
        ban_button = QPushButton("Ban User")
        mute_button = QPushButton("Mute User")
        temp_ban_button = QPushButton("Temporary Ban User")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(moderation_label)
        layout.addWidget(ban_button)
        layout.addWidget(mute_button)
        layout.addWidget(temp_ban_button)

        self.setLayout(layout)