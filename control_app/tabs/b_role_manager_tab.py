from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QHBoxLayout

class RoleManagerTab(QWidget):
    def __init__(self, bot=None):
        super().__init__()
        self.bot = bot

        # role management
        role_label = QLabel("Manage Roles:")
        self.role_list = QListWidget()

        # buttons
        add_role_button = QPushButton("Add Role")
        delete_role_button = QPushButton("Delete Role")
        modify_role_button = QPushButton("Modify Role")

        # button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_role_button)
        button_layout.addWidget(delete_role_button)
        button_layout.addWidget(modify_role_button)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(role_label)
        layout.addWidget(self.role_list)
        layout.addLayout(button_layout)

        self.setLayout(layout)
