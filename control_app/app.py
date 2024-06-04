import sys
from PyQt5.QtWidgets import QApplication
from control_app.control_panel import BotControlPanel
from PyQt5.QtGui import QIcon

def load_stylesheet(stylesheet_path):
    try:
        with open(stylesheet_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Stylesheet {stylesheet_path} not found.")
        return ""

class BotControlApp(QApplication):
    def __init__(self, sys_argv, bot):
        super().__init__(sys_argv)
        self.setWindowIcon(QIcon("control_app/graphics/icon.png"))
        self.setStyleSheet(load_stylesheet("control_app/stylesheets/style.css"))
        self.panel = BotControlPanel(bot)

    def run(self):
        sys.exit(self.exec_())
