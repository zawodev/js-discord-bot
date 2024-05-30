from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit

class StatisticsTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # statistics
        statistics_label = QLabel("Server Statistics:")

        # buttons
        generate_report_button = QPushButton("Generate Report")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(statistics_label)
        layout.addWidget(generate_report_button)

        self.setLayout(layout)
