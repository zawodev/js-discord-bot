import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, \
    QListWidget, QTabWidget
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap


class BotControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Discord Bot Control Panel')
        self.setGeometry(100, 100, 800, 600)

        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap('background.jpg')
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.createWelcomeFarewellTab(), "Welcome/Farewell")
        self.tabs.addTab(self.createRoleManagementTab(), "Role Management")
        self.tabs.addTab(self.createModerationTab(), "Moderation")
        self.tabs.addTab(self.createRewardSystemTab(), "Reward System")
        self.tabs.addTab(self.createIntegrationTab(), "Integrations")
        self.tabs.addTab(self.createMiniGamesTab(), "Mini Games")
        self.tabs.addTab(self.createStatisticsTab(), "Statistics")
        self.tabs.addTab(self.createBackupTab(), "Backup")

        layout.addWidget(self.tabs)

        self.setLayout(layout)
        self.show()

    def createWelcomeFarewellTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome Message:")
        self.welcome_message = QTextEdit()

        farewell_label = QLabel("Farewell Message:")
        self.farewell_message = QTextEdit()

        save_button = QPushButton("Save Messages")
        save_button.clicked.connect(self.save_welcome_farewell_messages)

        layout.addWidget(welcome_label)
        layout.addWidget(self.welcome_message)
        layout.addWidget(farewell_label)
        layout.addWidget(self.farewell_message)
        layout.addWidget(save_button)

        tab.setLayout(layout)
        return tab

    def createRoleManagementTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        role_label = QLabel("Manage Roles:")
        self.role_list = QListWidget()

        add_role_button = QPushButton("Add Role")
        delete_role_button = QPushButton("Delete Role")
        modify_role_button = QPushButton("Modify Role")

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_role_button)
        button_layout.addWidget(delete_role_button)
        button_layout.addWidget(modify_role_button)

        layout.addWidget(role_label)
        layout.addWidget(self.role_list)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        return tab

    def createModerationTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        moderation_label = QLabel("Chat Moderation:")

        ban_button = QPushButton("Ban User")
        mute_button = QPushButton("Mute User")
        temp_ban_button = QPushButton("Temporary Ban User")

        layout.addWidget(moderation_label)
        layout.addWidget(ban_button)
        layout.addWidget(mute_button)
        layout.addWidget(temp_ban_button)

        tab.setLayout(layout)
        return tab

    def createRewardSystemTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        reward_label = QLabel("Reward System:")

        add_points_button = QPushButton("Add Points")
        remove_points_button = QPushButton("Remove Points")
        reward_exchange_button = QPushButton("Reward Exchange")

        layout.addWidget(reward_label)
        layout.addWidget(add_points_button)
        layout.addWidget(remove_points_button)
        layout.addWidget(reward_exchange_button)

        tab.setLayout(layout)
        return tab

    def createIntegrationTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        integration_label = QLabel("Integrations:")

        weather_button = QPushButton("Weather API")
        currency_button = QPushButton("Currency API")
        news_button = QPushButton("News API")

        layout.addWidget(integration_label)
        layout.addWidget(weather_button)
        layout.addWidget(currency_button)
        layout.addWidget(news_button)

        tab.setLayout(layout)
        return tab

    def createMiniGamesTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        minigames_label = QLabel("Mini Games:")

        quiz_button = QPushButton("Start Quiz")
        word_game_button = QPushButton("Start Word Game")

        layout.addWidget(minigames_label)
        layout.addWidget(quiz_button)
        layout.addWidget(word_game_button)

        tab.setLayout(layout)
        return tab

    def createStatisticsTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        statistics_label = QLabel("Server Statistics:")

        generate_report_button = QPushButton("Generate Report")

        layout.addWidget(statistics_label)
        layout.addWidget(generate_report_button)

        tab.setLayout(layout)
        return tab

    def createBackupTab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        backup_label = QLabel("Backup and Restore:")

        backup_button = QPushButton("Backup Data")
        restore_button = QPushButton("Restore Data")

        layout.addWidget(backup_label)
        layout.addWidget(backup_button)
        layout.addWidget(restore_button)

        tab.setLayout(layout)
        return tab

    def save_welcome_farewell_messages(self):
        welcome_msg = self.welcome_message.toPlainText()
        farewell_msg = self.farewell_message.toPlainText()
        print(f"Saved Welcome Message: {welcome_msg}")
        print(f"Saved Farewell Message: {farewell_msg}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            font-family: Arial, sans-serif;
            font-size: 14px;
        }
        QPushButton {
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            background-color: #007BFF;
            color: white;
            border: none;
        }
        QPushButton:hover {
            background-color: #0056b3;
        }
        QLabel {
            font-weight: bold;
            font-size: 16px;
        }
        QTextEdit, QListWidget {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 5px;
        }
    """)

    panel = BotControlPanel()
    sys.exit(app.exec_())
