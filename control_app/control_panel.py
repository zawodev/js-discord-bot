from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QPalette, QBrush, QPixmap

from control_app.tabs.welcome_goodbye_tab import WelcomeGoodbyeTab
from control_app.tabs.banned_words_tab import BannedWordsTab
from control_app.tabs.user_moderator_tab import UserModeratorTab
from control_app.tabs.reward_system_tab import RewardSystemTab
from control_app.tabs.api_integration_tab import ApiIntegrationTab
from control_app.tabs.statistics_tab import StatisticsTab
from control_app.tabs.settings_tab import SettingsTab

class BotControlPanel(QWidget):
    def __init__(self, bot):
        """
        Initialize the main control panel widget for a Discord bot.

        :param bot: The bot instance to control and interact with through the GUI.
        """
        super().__init__()

        # set window properties
        self.setWindowTitle('Discord Bot Control Panel')  # set the window title
        self.setGeometry(100, 100, 800, 600)  # set the window position and size

        # set up the background with a custom image
        background = QPixmap('control_app/graphics/background.jpg')  # load the background image
        self.setAutoFillBackground(True)  # enable background autofill for the widget
        palette = self.palette()  # get the widget's current palette
        palette.setBrush(QPalette.Window, QBrush(background))  # set the window's background brush
        self.setPalette(palette)  # apply the updated palette

        # initialize and configure the tab widget
        self.tabs = QTabWidget()  # create a tab widget
        self.tabs.setMovable(True)  # allow tabs to be repositioned by the user
        # add tabs for various bot control functions
        self.tabs.addTab(WelcomeGoodbyeTab(), "Welcome/Goodbye")
        self.tabs.addTab(BannedWordsTab(), "Banned Words")
        self.tabs.addTab(UserModeratorTab(bot=bot), "User Moderation")
        self.tabs.addTab(RewardSystemTab(bot=bot), "Reward System")
        self.tabs.addTab(ApiIntegrationTab(bot=bot), "YT API Integration")
        self.tabs.addTab(StatisticsTab(bot=bot), "Statistics")
        self.tabs.addTab(SettingsTab(bot=bot), "Settings")

        # set up the main layout for the widget
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)  # add the tab widget to the layout
        self.setLayout(layout)  # set the widget's layout

        self.show()  # display the widget
