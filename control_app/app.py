import sys
from PyQt5.QtWidgets import QApplication
from control_app.control_panel import BotControlPanel
from PyQt5.QtGui import QIcon

def load_stylesheet(stylesheet_path):
    """
    Loads a stylesheet from the given path.

    :param stylesheet_path: Path to the stylesheet file.
    :return: The content of the stylesheet file as a string. If the file is not found, returns an empty string.
    """
    try:
        with open(stylesheet_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Stylesheet {stylesheet_path} not found.")
        return ""

class BotControlApp(QApplication):
    """
    Custom QApplication subclass for the Bot Control application.
    """

    def __init__(self, sys_argv, bot):
        """
        Initializes the BotControlApp with the given system arguments and bot instance.

        :param sys_argv: Command line arguments passed to the application.
        :param bot: An instance of the bot to be controlled.
        """
        super().__init__(sys_argv)
        self.setWindowIcon(QIcon("control_app/graphics/icon.png"))
        self.setStyleSheet(load_stylesheet("control_app/stylesheets/style.css"))
        self.panel = BotControlPanel(bot)

    def run(self):
        """
        Starts the application event loop.

        :returns: This function does not return; it calls sys.exit() to terminate the program when the event loop ends.
        """
        sys.exit(self.exec_())
