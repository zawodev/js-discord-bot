from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit

class BackupTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # backup and restore
        backup_label = QLabel("Backup and Restore:")

        # buttons
        backup_button = QPushButton("Backup Data")
        restore_button = QPushButton("Restore Data")

        # layout
        layout = QVBoxLayout()
        layout.addWidget(backup_label)
        layout.addWidget(backup_button)
        layout.addWidget(restore_button)

        self.setLayout(layout)