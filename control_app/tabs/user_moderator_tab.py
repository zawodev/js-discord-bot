import asyncio
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QHBoxLayout, QInputDialog, QDialog, QLineEdit, QDoubleSpinBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import requests

from control_app.timeout_dialog import TimeoutDialog
from utils.url_to_pixmap import url_to_pixmap
from utils.saving_loading_json import load_setting_json, save_setting_json


class UserModeratorTab(QWidget):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.user_data = {}  # dictionary to store user data
        self.moderator = bot.get_cog('UserModerator')

        self.punishments = {'ban': 0, 'kick': 0, 'timeout': 0}
        self.load_punishment_settings()

        # edit ban, kick, timeout penalty
        edit_penalty_layout = QHBoxLayout()
        labels = ['Ban Penalty', 'Kick Penalty', 'Timeout Penalty']
        self.spinboxes = []
        for idx, label in enumerate(labels):
            spinbox = QDoubleSpinBox()
            spinbox.setValue(round(self.punishments[list(self.punishments)[idx]], 2))
            spinbox.setDecimals(2)
            spinbox.setSingleStep(0.01)
            spinbox.setMaximum(999.99)
            spinbox.setMinimum(-999.99)
            self.spinboxes.append(spinbox)
            edit_penalty_layout.addWidget(QLabel(label))
            edit_penalty_layout.addWidget(spinbox)


        # layout
        self.layout = QVBoxLayout()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)
        self.layout.addLayout(edit_penalty_layout)


        # fetch butto0ns always at the bottom
        self.fetch_button = QPushButton("Refresh Users")
        self.fetch_button.setStyleSheet("position: absolute; bottom: 10px;")
        self.fetch_button.clicked.connect(self.handle_fetch_click)
        self.layout.addWidget(self.fetch_button, alignment=Qt.AlignBottom)

        self.save_punishment_btn = QPushButton("Save Punishment")
        self.save_punishment_btn.clicked.connect(self.save_punishment_settings)
        self.layout.addWidget(self.save_punishment_btn, alignment=Qt.AlignBottom)

        self.handle_fetch_click()
        self.setLayout(self.layout)

    # ------------------------------------ button click handlers ------------------------------------

    def load_punishment_settings(self):
        try:
            punishment_settings = load_setting_json('punishment_settings') or {'ban': 0, 'kick': 0, 'timeout': 0}
            self.punishments = {key: value for key, value in punishment_settings.items()}
        except Exception as e:
            print(f"Error loading punishment settings: {e}")

    def save_punishment_settings(self):
        try:
            for idx, key in enumerate(self.punishments):
                self.punishments[key] = self.spinboxes[idx].value()
            save_setting_json('punishment_settings', self.punishments)
            QMessageBox.information(self, "Success", "User punishment settings saved successfully!")
        except Exception as e:
            print(f"Error saving punishment settings: {e}")

    # ------------------------------------ button click handlers ------------------------------------
    def handle_fetch_click(self):
        self.user_data = load_setting_json('user_data')
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
        await self.moderator.ban_user(user_id, reason)

    async def kick_user_async(self, user_id, reason):
        await self.moderator.kick_user(user_id, reason)

    async def timeout_user_async(self, user_id, reason, duration):
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
        for user_id, user_info in self.user_data.items():
            user_layout = QHBoxLayout()

            # avatar
            avatar_label = QLabel()
            avatar_pixmap = url_to_pixmap(user_info.get('avatar_url'), 50, 50)
            if avatar_pixmap:
                avatar_label.setPixmap(avatar_pixmap)
            user_layout.addWidget(avatar_label)

            # username and id
            user_label = QLabel(f"{user_info.get('name')} ({user_id})")
            user_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            user_layout.addWidget(user_label, 1)  # Make the user label expand to take available space

            # add a spacer to push the buttons to the right
            user_layout.addStretch()

            # ban button
            ban_button = QPushButton("Ban")
            ban_button.setFixedWidth(75)
            ban_button.clicked.connect(lambda _, uid=user_id: self.handle_ban_click(uid))
            if not user_info.get('is_on_server'):
                ban_button.setEnabled(False)
            user_layout.addWidget(ban_button)

            # kick button
            kick_button = QPushButton("Kick")
            kick_button.setFixedWidth(75)
            kick_button.clicked.connect(lambda _, uid=user_id: self.handle_kick_click(uid))
            if not user_info.get('is_on_server'):
                kick_button.setEnabled(False)
            user_layout.addWidget(kick_button)

            # timeout button
            timeout_button = QPushButton("Mute") # "Timeout" wouldn't fit on screen
            timeout_button.setFixedWidth(75)
            timeout_button.clicked.connect(lambda _, uid=user_id: self.handle_timeout_click(uid))
            if not user_info.get('is_on_server'):
                timeout_button.setEnabled(False)
            user_layout.addWidget(timeout_button)

            self.scroll_layout.addLayout(user_layout)
