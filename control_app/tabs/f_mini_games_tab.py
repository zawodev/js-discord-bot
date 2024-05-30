from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit

class MiniGamesTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # minigames
        minigames_label = QLabel("Mini Games:")

        # buttons
        quiz_button = QPushButton("Start Quiz")
        word_game_button = QPushButton("Start Word Game")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(minigames_label)
        layout.addWidget(quiz_button)
        layout.addWidget(word_game_button)

        self.setLayout(layout)
