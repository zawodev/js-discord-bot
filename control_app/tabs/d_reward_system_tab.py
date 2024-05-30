from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class RewardSystemTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # reward system
        reward_label = QLabel("Reward System:")

        # buttons
        add_points_button = QPushButton("Add Points")
        remove_points_button = QPushButton("Remove Points")
        reward_exchange_button = QPushButton("Reward Exchange")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(reward_label)
        layout.addWidget(add_points_button)
        layout.addWidget(remove_points_button)
        layout.addWidget(reward_exchange_button)

        self.setLayout(layout)
