import sys
from PyQt5.QtWidgets import QApplication
from control_app.control_panel import BotControlPanel

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
        # self.bot = bot
        self.setStyleSheet(load_stylesheet("control_app/style.css"))
        self.panel = BotControlPanel(bot)

    def run(self):
        sys.exit(self.exec_())
