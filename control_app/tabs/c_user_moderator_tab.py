import asyncio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QFormLayout, QFrame
from PyQt5.QtCore import Qt


class UserModeratorTab(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.users = {}  # Dictionary to store user data

        layout = QVBoxLayout()

        # Create a scroll area to display users
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QFormLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Create the fetch button and set its style to always be at the bottom
        self.fetch_button = QPushButton("Fetch Users")
        self.fetch_button.setStyleSheet("position: absolute; bottom: 10px;")
        layout.addWidget(self.fetch_button, alignment=Qt.AlignBottom)

        self.fetch_button.clicked.connect(self.my_fetch_users)
        self.setLayout(layout)

    def my_fetch_users(self):
        asyncio.run(self.fetch_users_async())

    async def fetch_users_async(self):
        try:
            self.users = {}
            users = await self.bot.get_cog('UserModerator').fetch_users()
            if users:
                self.users = users
                self.display_users()
        except Exception as e:
            print(f'Error: {e}')

    def display_users(self):
        # Clear the previous user list
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Display each user in the form layout
        for user_id, user_info in self.users.items():
            user_label = QLabel(f'User ID: {user_id}, Info: {user_info}')
            self.scroll_layout.addRow(user_label)

    def ban_user(self, user_id):
        # Logic to ban user with user_id
        pass

    def kick_user(self, user_id):
        # Logic to kick user with user_id
        pass

    def mute_user(self, user_id):
        # Logic to mute user with user_id
        pass
