import asyncio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal, QObject

from control_app.change_points_dialog import ChangePointsDialog

class RewardSystemTab(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild_users = {}  # dictionary to store user data
        self.user_fetcher = bot.get_cog('UserFetcher')
        self.reward_system = bot.get_cog('RewardSystem')
        # self.reward_system.user_modified.connect(self.display_users)

        # layout
        self.layout = QVBoxLayout(self)

        # table widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Username, Behavioural Points, Reward Points, Actions
        self.table.setHorizontalHeaderLabels(['Username', 'Behavioural Points', 'Reward Points', 'Actions'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)  # Enable sorting

        self.layout.addWidget(self.table)

        # fetch button always at the bottom
        self.fetch_button = QPushButton("Fetch Users")
        self.fetch_button.clicked.connect(self.handle_fetch_click)
        self.layout.addWidget(self.fetch_button, alignment=Qt.AlignBottom)

        self.handle_fetch_click()

    def handle_fetch_click(self):
        self.guild_users = asyncio.run(self.user_fetcher.fetch_users())
        self.display_users()

    def display_users(self):
        self.table.setRowCount(len(self.guild_users))
        sorted_users = sorted(self.guild_users.items(), key=lambda x: x[1].get('behaviour_points', 0), reverse=True)

        for row, (user_id, user_info) in enumerate(sorted_users):
            self.table.setRowHeight(row, 40)  # Adjusted row height

            # username
            self.table.setItem(row, 0, QTableWidgetItem(f"{user_info.get('username')} ({user_id})"))

            # behavioural points
            behaviour_points = QTableWidgetItem(f"{user_info.get('behaviour_points', 0):.2f}")
            behaviour_points.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, behaviour_points)

            # reward points
            reward_points = QTableWidgetItem(f"{user_info.get('reward_points', 0):.2f}")
            reward_points.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, reward_points)

            # Single button for both changes
            change_values_button = QPushButton("Change Values")
            change_values_button.clicked.connect(lambda _, uid=user_id: self.change_points_dialog(uid))
            self.table.setCellWidget(row, 3, change_values_button)

        self.table.setSortingEnabled(True)  # Enable sorting after filling the table

    def change_points_dialog(self, user_id):
        dialog = ChangePointsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            behaviour_points, reward_points = dialog.get_data()
            self.reward_system.modify_user(user_id, {'behaviour_points': behaviour_points, 'reward_points': reward_points})
            self.display_users()
