from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class ApiIntegrationTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # integrations
        integration_label = QLabel("Integrations:")

        # buttons
        weather_button = QPushButton("Weather API")
        currency_button = QPushButton("Currency API")
        news_button = QPushButton("News API")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(integration_label)
        layout.addWidget(weather_button)
        layout.addWidget(currency_button)
        layout.addWidget(news_button)

        self.setLayout(layout)
