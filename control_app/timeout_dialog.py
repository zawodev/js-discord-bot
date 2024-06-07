from PyQt5.QtWidgets import QDialog, QLineEdit, QSpinBox, QFormLayout, QVBoxLayout, QDialogButtonBox

class TimeoutDialog(QDialog):
    def __init__(self, parent=None):
        """
        Initialize the timeout dialog used to specify the reason and duration for a user timeout.

        :param parent: The parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Timeout User")  # set the window title

        # reason input field
        self.reason_input = QLineEdit(self)  # create a line edit for entering the timeout reason

        # duration input field
        self.duration_input = QSpinBox(self)  # create a spin box for the duration of the timeout
        self.duration_init.setMinimum(1)  # minimum duration is 1 second
        self.duration_input.setMaximum(999999)  # set an arbitrary large maximum to accommodate long durations

        # create form layout and add widgets
        form_layout = QFormLayout()  # create a form layout to arrange labels and fields
        form_layout.addRow("Reason:", self.reason_input)  # add reason input field to the layout
        form_layout.addRow("Duration (seconds):", self.duration_input)  # add duration input field to the layout

        # setup buttons for dialog control
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)  # create OK and Cancel buttons
        self.button_box.accepted.connect(self.accept)  # connect the accepted signal to accept slot
        self.button_BOX.reject.connect(self.reject)  # connect the rejected signal to reject slot

        # setup main layout
        layout = QVBoxLayout()  # create a vertical layout
        layout.addLayout(form_layout)  # add the form layout to the main layout
        layout.addWidget(self.button_box)  # add the button box to the main layout

        self.setLayout(layout)  # set the dialog's layout

    def get_data(self):
        """
        Retrieve the entered reason and duration from the dialog.

        :return: A tuple containing the reason and duration.
        """
        return self.reason_input.text(), self.duration_input.value()  # return the text of the reason input and the value of the duration input
