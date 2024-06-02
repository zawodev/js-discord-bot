from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QTextEdit
from PyQt5.QtGui import QPixmap
from utils.saving_loading_json import load_setting_json, save_setting_json
from utils.url_to_pixmap import url_to_pixmap
from datetime import datetime, timezone
import humanize


class ApiIntegrationTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot
        self.external_api = bot.get_cog('ExternalAPI')
        self.video_info = self.external_api.video_info

        # Main layout
        main_layout = QVBoxLayout()

        # Upper layout split into two parts
        upper_layout = QHBoxLayout()

        # Left layout for text information
        text_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.description_label = QLabel()
        self.published_at_label = QLabel()
        self.channel_title_label = QLabel()

        # Make text wrap in labels
        self.title_label.setWordWrap(True)
        self.description_label.setWordWrap(True)
        self.published_at_label.setWordWrap(True)
        self.channel_title_label.setWordWrap(True)

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.description_label)
        text_layout.addWidget(self.published_at_label)
        text_layout.addWidget(self.channel_title_label)

        # Right layout for the thumbnail
        thumbnail_layout = QVBoxLayout()
        self.thumbnail_label = QLabel()
        thumbnail_layout.addWidget(self.thumbnail_label)

        upper_layout.addLayout(text_layout)
        upper_layout.addLayout(thumbnail_layout)

        main_layout.addLayout(upper_layout)

        # Inputs layout
        inputs_layout = QVBoxLayout()
        self.url_label = QLabel("YouTube Channel URL or Name (like 'standupmaths' or 'EminemMusic'):")
        self.url_input = QLineEdit()
        self.discord_channel_label = QLabel("Discord Channel Name:")
        self.discord_channel_input = QLineEdit()
        self.notification_label = QLabel("Notification Message:")
        self.notification_input = QTextEdit()

        inputs_layout.addWidget(self.url_label)
        inputs_layout.addWidget(self.url_input)
        inputs_layout.addWidget(self.discord_channel_label)
        inputs_layout.addWidget(self.discord_channel_input)
        inputs_layout.addWidget(self.notification_label)
        inputs_layout.addWidget(self.notification_input)

        main_layout.addLayout(inputs_layout)

        # Buttons layout (bottom of the screen)
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.test_button = QPushButton("Check for new video")
        self.test_button.clicked.connect(self.check_for_new_video)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.test_button)

        main_layout.addLayout(buttons_layout)

        # Load initial settings
        self.load_settings()
        self.update_video_info()
        self.setLayout(main_layout)

    def load_settings(self):
        try:
            settings = load_setting_json('api_integration_settings')
            self.url_input.setText(settings['youtube_channel_name_or_url'])
            self.discord_channel_input.setText(settings['discord_channel_name'])
            self.notification_input.setPlainText(settings['notification_message'])
        except Exception as e:
            print(f'Failed to load settings: {e}')

    def save_settings(self):
        youtube_url = self.url_input.text()
        discord_channel = self.discord_channel_input.text()
        notification_message = self.notification_input.toPlainText()

        save_setting_json('api_integration_settings', {
            'youtube_channel_name_or_url': youtube_url,
            'discord_channel_name': discord_channel,
            'notification_message': notification_message
        })

        self.external_api.update_settings()

        QMessageBox.information(self, "Success", "Settings saved successfully.")

    def check_for_new_video(self):
        self.external_api.check_for_new_video()
        self.video_info = self.external_api.video_info
        self.update_video_info()

    def update_video_info(self):
        # Update UI with video info
        if self.video_info:
            snippet = self.video_info['snippet']
            self.title_label.setText(f"Title: {snippet['title']}")
            self.description_label.setText(f"Description: {snippet['description']}")
            self.published_at_label.setText(f"Published: {self.time_since(snippet['publishedAt'])}")
            self.channel_title_label.setText(f"Channel: {snippet['channelTitle']}")

            # Load the highest quality thumbnail
            thumbnails = snippet['thumbnails']
            highest_quality_thumbnail = thumbnails['high']['url']
            pixmap = url_to_pixmap(highest_quality_thumbnail, 320, 240)
            self.thumbnail_label.setPixmap(pixmap)
        else:
            self.title_label.setText("No video information available")
            self.description_label.setText("")
            self.published_at_label.setText("")
            self.channel_title_label.setText("")
            self.thumbnail_label.clear()

    def time_since(self, published_at):
        # Calculate the time since the video was published
        published_at_datetime = datetime.fromisoformat(published_at.replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - published_at_datetime
        return humanize.naturaltime(delta)
