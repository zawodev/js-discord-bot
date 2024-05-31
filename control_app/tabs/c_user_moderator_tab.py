import asyncio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QHBoxLayout, QInputDialog, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import requests

from control_app.timeout_dialog import TimeoutDialog


def get_avatar_pixmap(url):
    if not url:
        return QPixmap("control_app/discordgrey.png").scaled(50, 50, Qt.KeepAspectRatio)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = QImage()
            image.loadFromData(response.content)
            return QPixmap(image).scaled(50, 50, Qt.KeepAspectRatio)
    except Exception as e:
        print(f'error loading avatar: {e}')
    return QPixmap("control_app/discordgrey.png").scaled(50, 50, Qt.KeepAspectRatio)


class UserModeratorTab(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild_users = {}  # dictionary to store user data
        self.moderator = bot.get_cog('UserModerator')
        self.user_fetcher = bot.get_cog('UserFetcher')

        # layout
        self.layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        # fetch button always at the bottom
        self.fetch_button = QPushButton("Fetch Users")
        self.fetch_button.setStyleSheet("position: absolute; bottom: 10px;")
        self.fetch_button.clicked.connect(self.handle_fetch_click)
        self.layout.addWidget(self.fetch_button, alignment=Qt.AlignBottom)

        self.handle_fetch_click()
        self.setLayout(self.layout)

    # ------------------------------------ button click handlers ------------------------------------
    def handle_fetch_click(self):
        self.guild_users = asyncio.run(self.user_fetcher.fetch_users())
        self.display_users()

    def handle_ban_click(self, user_id):
        reason, ok_pressed = QInputDialog.getText(self, "Ban User", "Enter reason for banning:")
        if ok_pressed:
            self.bot.loop.create_task(self.ban_user_async(user_id, reason))

    def handle_kick_click(self, user_id):
        reason, ok_pressed = QInputDialog.getText(self, "Kick User", "Enter reason for kicking:")
        if ok_pressed:
            self.bot.loop.create_task(self.kick_user_async(user_id, reason))

    def handle_timeout_click(self, user_id):
        dialog = TimeoutDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            reason, duration = dialog.get_data()
            self.bot.loop.create_task(self.timeout_user_async(user_id, reason, duration))

    # ------------------------------------ button click asyncs ------------------------------------
    async def ban_user_async(self, user_id, reason):
        print(f"banning user {user_id}")
        await self.moderator.ban_user(user_id, reason)

    async def kick_user_async(self, user_id, reason):
        print(f"kicking user {user_id}")
        await self.moderator.kick_user(user_id, reason)

    async def timeout_user_async(self, user_id, reason, duration):
        print(f"timing out user {user_id}")
        await self.moderator.timeout_user(user_id, reason, duration)

    # ------------------------------------ display users ---------------------------------
    def display_users(self):
        # clear the layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout = item.layout()
                if layout is not None:
                    while layout.count():
                        sub_item = layout.takeAt(0)
                        sub_widget = sub_item.widget()
                        if sub_widget is not None:
                            sub_widget.deleteLater()

        # display each user in the layout
        for user_id, user_info in self.guild_users.items():
            user_layout = QHBoxLayout()

            # avatar
            avatar_label = QLabel()
            avatar_pixmap = get_avatar_pixmap(user_info.get('avatar_url'))
            if avatar_pixmap:
                avatar_label.setPixmap(avatar_pixmap)
            user_layout.addWidget(avatar_label)

            # username and id
            user_label = QLabel(f"{user_info.get('username')} ({user_id})")
            user_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            user_layout.addWidget(user_label, 1)  # Make the user label expand to take available space

            # add a spacer to push the buttons to the right
            user_layout.addStretch()

            # ban button
            ban_button = QPushButton("Ban")
            ban_button.setFixedWidth(75)
            ban_button.clicked.connect(lambda _, uid=user_id: self.handle_ban_click(uid))
            user_layout.addWidget(ban_button)

            # kick button
            kick_button = QPushButton("Kick")
            kick_button.setFixedWidth(75)
            kick_button.clicked.connect(lambda _, uid=user_id: self.handle_kick_click(uid))
            user_layout.addWidget(kick_button)

            # timeout button
            timeout_button = QPushButton("Mute") # "Timeout" wouldn't fit on screen
            timeout_button.setFixedWidth(75)
            timeout_button.clicked.connect(lambda _, uid=user_id: self.handle_timeout_click(uid))
            user_layout.addWidget(timeout_button)

            self.scroll_layout.addLayout(user_layout)
