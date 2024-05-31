from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QHBoxLayout, QCheckBox, QInputDialog, QMessageBox, QLineEdit
from utils.banned_words import save_banned_words, load_banned_words
from utils.settings import save_setting, load_setting

class BannedWordsTab(QWidget):
    def __init__(self):
        super().__init__()

        # Load banned words from file
        self.banned_words = load_banned_words()

        # banned words
        title = QLabel("Banned Words:")
        self.role_list = QListWidget()
        self.role_list.addItems(self.banned_words)

        # Check for links checkbox
        self.link_checkbox = QCheckBox("Check For Links")
        self.link_checkbox.setChecked(load_setting("check_for_links").lower() == "true")
        self.link_checkbox.stateChanged.connect(lambda: save_setting("check_for_links", str(self.link_checkbox.isChecked()).lower()))

        # buttons
        add_role_button = QPushButton("Add word")
        delete_role_button = QPushButton("Remove word")
        modify_role_button = QPushButton("Modify word")

        # Connect buttons to their functions
        add_role_button.clicked.connect(self.add_word)
        delete_role_button.clicked.connect(self.remove_word)
        modify_role_button.clicked.connect(self.modify_word)

        # button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_role_button)
        button_layout.addWidget(delete_role_button)
        button_layout.addWidget(modify_role_button)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.role_list)
        layout.addWidget(self.link_checkbox)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def add_word(self):
        text, ok = QInputDialog.getText(self, 'Add word', 'Enter a word:')
        if ok and text:
            if not self.word_exists(text):
                self.role_list.addItem(text)
                self.banned_words.append(text)
                self.save_banned_words()
            else:
                self.show_message("Error", "This word already exists!")

    def remove_word(self):
        list_items = self.role_list.selectedItems()
        if not list_items: return
        for item in list_items:
            self.role_list.takeItem(self.role_list.row(item))
            self.banned_words.remove(item.text())
        self.save_banned_words()

    def modify_word(self):
        list_items = self.role_list.selectedItems()
        if not list_items: return
        item = list_items[0]
        text, ok = QInputDialog.getText(self, 'Modify word', 'Modify word:', QLineEdit.Normal, item.text())
        if ok and text:
            if not self.word_exists(text) or text == item.text():
                item.setText(text)
                self.banned_words[self.role_list.row(item)] = text
                self.save_banned_words()
            else:
                self.show_message("Error", "This word already exists!")

    def word_exists(self, word):
        return word in self.banned_words

    def save_banned_words(self):
        save_banned_words(self.banned_words)

    def show_message(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.move(self.mapToGlobal(self.rect().center()) - msg_box.rect().center())
        msg_box.exec_()
