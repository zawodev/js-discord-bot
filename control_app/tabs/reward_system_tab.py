from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QHeaderView
from PyQt5.QtCore import Qt
from control_app.change_points_dialog import ChangePointsDialog
from utils.saving_loading_json import load_setting_json, save_setting_json

class QTableWidgetItemNumeric(QTableWidgetItem):
    """
    A custom QTableWidgetItem that stores numeric values for proper sorting.
    """

    def __init__(self, value):
        """
        Initializes the QTableWidgetItemNumeric with a numeric value.

        :param value: The numeric value to be displayed and stored.
        """
        display_value = f"{value:.2f}"
        super().__init__(display_value)
        self.value = value

    def __lt__(self, other):
        """
        Compares this item with another item for sorting.

        :param other: The other QTableWidgetItem to compare against.
        :returns: True if this item's value is less than the other item's value.
        """
        if isinstance(other, QTableWidgetItemNumeric):
            return self.value < other.value
        return super().__lt__(other)

class RewardSystemTab(QWidget):
    """
    A QWidget subclass that provides an interface for the reward system.

    :param bot: The bot instance to interact with the bot's functionalities.
    """

    def __init__(self, bot):
        """
        Initializes the RewardSystemTab widget.

        :param bot: The bot instance to interact with the bot's functionalities.
        """
        super().__init__()
        self.bot = bot
        self.user_data = load_setting_json('user_data')
        self.reward_system = bot.get_cog('RewardSystem')

        # layout
        self.layout = QVBoxLayout(self)

        # table widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Username, Messages Count, Is On Server, Behavioural Points, Reward Points, Actions
        self.table.setHorizontalHeaderLabels(['Username', 'Messages Count', 'Is On Server', 'Behavioural Points', 'Reward Points', 'Actions'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)  # Enable sorting

        self.layout.addWidget(self.table)

        # fetch button always at the bottom
        self.fetch_button = QPushButton("Refresh")
        self.fetch_button.clicked.connect(self.handle_refresh_click)
        self.layout.addWidget(self.fetch_button, alignment=Qt.AlignBottom)

        self.display_users()

    def handle_refresh_click(self):
        """
        Handles the click event of the refresh button to update user data.
        """
        self.user_data = load_setting_json('user_data')  # field for is user in guild now
        try:
            self.update_users()
        except Exception as e:
            print(f"Error updating users: {e}")

    def display_users(self):
        """
        Displays the user data in the table widget.
        """
        self.table.setRowCount(len(self.user_data))

        for row, (user_id, user_info) in enumerate(self.user_data.items()):
            self.table.setRowHeight(row, 40)

            # username
            self.table.setItem(row, 0, QTableWidgetItem(f"{user_info.get('name')} ({user_id})"))

            # messages count
            messages_count = QTableWidgetItemNumeric(user_info.get('messages_count', 0))
            messages_count.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, messages_count)

            # is on server
            is_on_server = QTableWidgetItem("Yes" if user_info.get('is_on_server', False) else "No")
            is_on_server.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, is_on_server)

            # behavioural points
            behaviour_points = QTableWidgetItemNumeric(user_info.get('behaviour_points', 0))
            behaviour_points.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, behaviour_points)

            # reward points
            reward_points = QTableWidgetItemNumeric(user_info.get('reward_points', 0))
            reward_points.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 4, reward_points)

            # Single button for both changes
            change_values_button = QPushButton("Modify")
            change_values_button.clicked.connect(lambda _, uid=user_id: self.change_points_dialog(uid))
            self.table.setCellWidget(row, 5, change_values_button)

    def update_users(self):
        """
        Updates the user data in the table widget without recreating it.
        """
        self.table.setSortingEnabled(False)
        for row, (user_id, user_info) in enumerate(self.user_data.items()):
            # get user id from table item column 0
            og_user_id = self.table.item(row, 0).text().split(' ')[-1][1:-1]

            # messages count
            self.table.item(row, 1).setText(str(self.user_data[str(og_user_id)].get('messages_count', 0)))

            # is on server
            is_on_server = "Yes" if self.user_data[str(og_user_id)].get('is_on_server', False) else "No"
            self.table.item(row, 2).setText(is_on_server)

            # behavioural points
            self.table.item(row, 3).setText(f"{self.user_data[str(og_user_id)].get('behaviour_points', 0):.2f}")

            # reward points
            self.table.item(row, 4).setText(f"{self.user_data[str(og_user_id)].get('reward_points', 0):.2f}")
        self.table.setSortingEnabled(True)

    def change_points_dialog(self, user_id):
        """
        Opens a dialog to change the points of a user and updates the table after changes.

        :param user_id: The ID of the user whose points are to be changed.
        """
        dialog = ChangePointsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            behaviour_points, reward_points = dialog.get_data()
            self.reward_system.modify_user(user_id, {'behaviour_points': behaviour_points, 'reward_points': reward_points})
            self.handle_refresh_click()
