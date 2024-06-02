from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap

from control_app.tabs.welcome_goodbye_tab import WelcomeGoodbyeTab
from control_app.tabs.banned_words_tab import BannedWordsTab
from control_app.tabs.user_moderator_tab import UserModeratorTab
from control_app.tabs.reward_system_tab import RewardSystemTab
from control_app.tabs.api_integration_tab import ApiIntegrationTab
from control_app.tabs.statistics_tab import StatisticsTab
from control_app.tabs.fetch_data_tab import FetchData

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
        self.tabs.addTab(StatisticsTab(bot=bot), "Statistics")
        self.tabs.addTab(FetchData(bot=bot), "Fetch Data")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.show()
