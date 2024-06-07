from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QHBoxLayout, QCheckBox, QInputDialog, QMessageBox, QLineEdit
from utils.saving_loading_json import save_setting_json, load_setting_json

class BannedWordsTab(QWidget):
    """
    A QWidget subclass that provides an interface for managing banned words and link checking settings.
    """

    def __init__(self):
        """
        Initializes the BannedWordsTab widget.
        """
        super().__init__()

        # init first time
        self.banned_words = []
        self.link_checkbox = QCheckBox("Check For Links")
        self.load_settings()

        # banned words
        title = QLabel("Banned Words:")
        self.word_list = QListWidget()
        self.word_list.addItems(self.banned_words)

        # Check for links checkbox
        self.link_checkbox.stateChanged.connect(lambda: save_setting_json("banned_words_settings", {"check_for_links": str(self.link_checkbox.isChecked()).lower()}))

        # buttons
        add_role_button = QPushButton("Add word")
        delete_role_button = QPushButton("Remove word")
        modify_role_button = QPushButton("Modify word")

        # connect buttons to their functions
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
        layout.addWidget(self.word_list)
        layout.addWidget(self.link_checkbox)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def load_settings(self):
        """
        Loads settings from JSON files and populates the UI elements with the loaded values.
        """
        try:
            settings = load_setting_json('banned_words_settings')
            self.link_checkbox.setChecked(settings['check_for_links'].lower() == "true")
            banned_words_list = load_setting_json('banned_words')
            self.banned_words = banned_words_list
        except Exception as e:
            print(f'Failed to load settings: {e}')

    def add_word(self):
        """
        Prompts the user to enter a new banned word and adds it to the list if it doesn't already exist.
        """
        text, ok = QInputDialog.getText(self, 'Add word', 'Enter a word:')
        if ok and text:
            if not self.word_exists(text):
                self.word_list.addItem(text)
                self.banned_words.append(text)
                self.save_banned_words()
            else:
                self.show_message("Error", "This word already exists!")

    def remove_word(self):
        """
        Removes the selected word(s) from the list.
        """
        list_items = self.word_list.selectedItems()
        if not list_items: return
        for item in list_items:
            self.word_list.takeItem(self.word_list.row(item))
            self.banned_words.remove(item.text())
        self.save_banned_words()

    def modify_word(self):
        """
        Prompts the user to modify the selected word and updates the list if the new word doesn't already exist.
        """
        list_items = self.word_list.selectedItems()
        if not list_items: return
        item = list_items[0]
        text, ok = QInputDialog.getText(self, 'Modify word', 'Modify word:', QLineEdit.Normal, item.text())
        if ok and text:
            if not self.word_exists(text) or text == item.text():
                item.setText(text)
                self.banned_words[self.word_list.row(item)] = text
                self.save_banned_words()
            else:
                self.show_message("Error", "This word already exists!")

    def word_exists(self, word):
        """
        Checks if a word already exists in the banned words list.

        :param word: The word to check.
        :returns: True if the word exists, False otherwise.
        """
        return word in self.banned_words

    def save_banned_words(self):
        """
        Saves the banned words list to a JSON file.
        """
        save_setting_json('banned_words', self.banned_words)

    def show_message(self, title, message):
        """
        Displays a message box with the given title and message.

        :param title: The title of the message box.
        :param message: The message to display.
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.addButton(QMessageBox.Ok)
        msg_box.move(self.mapToGlobal(self.rect().center()) - msg_box.rect().center())
        msg_box.exec_()
