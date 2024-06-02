import asyncio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QHeaderView
from PyQt5.QtCore import Qt

from control_app.change_points_dialog import ChangePointsDialog
from utils.saving_loading_json import load_setting_json, save_setting_json

class RewardSystemTab(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild_users = load_setting_json('user_data')
        self.user_fetcher = bot.get_cog('UserFetcher')
        self.reward_system = bot.get_cog('RewardSystem')

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
        self.fetch_button = QPushButton("Refresh")
        self.fetch_button.clicked.connect(self.handle_refresh_click)
        self.layout.addWidget(self.fetch_button, alignment=Qt.AlignBottom)

        self.display_users()

    def handle_refresh_click(self):
        self.guild_users = load_setting_json('user_data') # field for is user in guild now
        self.update_users()

    def display_users(self):
        self.table.setRowCount(len(self.guild_users))

        for row, (user_id, user_info) in enumerate(self.guild_users.items()):
            self.table.setRowHeight(row, 40)

            # username
            self.table.setItem(row, 0, QTableWidgetItem(f"{user_info.get('name')} ({user_id})"))

            # behavioural points
            behaviour_points = QTableWidgetItem(f"{user_info.get('behaviour_points', 0):.2f}")
            behaviour_points.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, behaviour_points)

            # reward points
            reward_points = QTableWidgetItem(f"{user_info.get('reward_points', 0):.2f}")
            reward_points.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, reward_points)

            # Single button for both changes
            change_values_button = QPushButton(f"Modify: {user_info.get("name", "")}")
            change_values_button.clicked.connect(lambda _, uid=user_id: self.change_points_dialog(uid))
            self.table.setCellWidget(row, 3, change_values_button)

    def update_users(self):
        # update the values in the existing table without recreating it
        for row in range(self.table.rowCount()):
            # get user_id from the username cell which contains (user_id)
            username_item = self.table.item(row, 0)
            user_id = username_item.text().split('(')[-1].split(')')[0]

            if user_id in self.guild_users:
                user_info = self.guild_users[user_id]

                # update behavioural points
                behaviour_points = self.table.item(row, 1)
                behaviour_points.setText(f"{user_info.get('behaviour_points', 0):.2f}")

                # update reward points
                reward_points = self.table.item(row, 2)
                reward_points.setText(f"{user_info.get('reward_points', 0):.2f}")

    def change_points_dialog(self, user_id):
        dialog = ChangePointsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            behaviour_points, reward_points = dialog.get_data()
            self.reward_system.modify_user(user_id, {'behaviour_points': behaviour_points, 'reward_points': reward_points})
            self.handle_refresh_click()
