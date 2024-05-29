import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTabWidget, QVBoxLayout, QWidget)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Discord Bot Control Panel')
        self.setGeometry(100, 100, 800, 600)

        self.background = QPixmap('background.jpg')

        self.tab_widget = CustomTabWidget(self)
        self.tab_widget.addTab(WelcomeTab(), "Powitania i Pożegnania")
        self.tab_widget.addTab(RoleManagementTab(), "Zarządzanie Rolami")
        self.tab_widget.addTab(ChatModerationTab(), "Moderacja Czatu")
        self.tab_widget.addTab(RewardsSystemTab(), "System Nagród")

        self.setCentralWidget(self.tab_widget)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

class CustomTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabPosition(QTabWidget.North)
        self.setMovable(True)
        self.setStyleSheet("""
            QTabBar::tab { 
                height: 25px; 
                width: 200px; 
                background: rgba(255, 255, 255, .9);
                color: black; 
                border: 2px solid black;
            }
            QTabWidget::pane {
                border: none;
                background: transparent;
            }
        """)

class TransparentButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 5px;
                background-color: rgba(0, 123, 255, 0.9);
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(0, 86, 179, 0.7);
            }
        """)

class WelcomeTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(TransparentButton('Configure Welcome Messages'))
        layout.addWidget(TransparentButton('Configure Goodbye Messages'))
        self.setLayout(layout)

class RoleManagementTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(TransparentButton('Add Role'))
        layout.addWidget(TransparentButton('Remove Role'))
        layout.addWidget(TransparentButton('Modify Roles'))
        self.setLayout(layout)

class ChatModerationTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(TransparentButton('Delete Vulgar Messages'))
        layout.addWidget(TransparentButton('Mute Users'))
        self.setLayout(layout)

class RewardsSystemTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(TransparentButton('Assign Points'))
        layout.addWidget(TransparentButton('Exchange Points'))
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QWidget {
            font-family: Arial, sans-serif;
            font-size: 14px;
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
        QTabBar::scroller {
            width: 40px;
        }
    """)

    window = MainWindow()
    sys.exit(app.exec_())
