from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap

from control_app.tabs.a_welcome_goodbye_tab import WelcomeGoodbyeTab
from control_app.tabs.b_banned_words_tab import BannedWordsTab
from control_app.tabs.c_user_moderator_tab import UserModeratorTab
from control_app.tabs.d_reward_system_tab import RewardSystemTab
from control_app.tabs.e_api_integration_tab import ApiIntegrationTab
from control_app.tabs.f_mini_games_tab import MiniGamesTab
from control_app.tabs.g_statistics_tab import StatisticsTab
from control_app.tabs.h_backup_tab import BackupTab


class BotControlPanel(QWidget):
    def __init__(self, bot):
        super().__init__()

        # window settings
        self.setWindowTitle('Discord Bot Control Panel')
        self.setGeometry(100, 100, 800, 600)

        # background
        background = QPixmap('control_app/background.jpg')
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

        # tab widgets
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.addTab(WelcomeGoodbyeTab(), "Welcome/Goodbye")
        self.tabs.addTab(BannedWordsTab(), "Banned Words")
        self.tabs.addTab(UserModeratorTab(bot=bot), "User Moderation")
        self.tabs.addTab(RewardSystemTab(bot=bot), "Reward System")
        self.tabs.addTab(ApiIntegrationTab(bot=bot), "Integrations")
        self.tabs.addTab(MiniGamesTab(bot=bot), "Mini Games")
        self.tabs.addTab(StatisticsTab(bot=bot), "Statistics")
        self.tabs.addTab(BackupTab(bot=bot), "Backup")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.show()
