from PyQt5.QtWidgets import QDialog, QDoubleSpinBox, QFormLayout, QVBoxLayout, QDialogButtonBox

class ChangePointsDialog(QDialog):
    def __init__(self, parent=None):
        """
        Initialize a dialog window for changing behaviour and reward points.

        :param parent: The parent widget of this dialog, default is None.
        """
        super().__init__(parent)
        self.setWindowTitle("Change Points")  # set window title

        # create and configure the double spin box for behaviour points
        self.behaviour_input = QDoubleSpinBox(self)
        self.behaviour_input.setRange(-1000.00, 1000.00)  # set minimum and maximum values
        self.behaviour_input.setDecimals(2)  # set the number of decimal places
        self.behaviour_input.setSingleStep(0.01)  # set the step size

        # create and configure the double spin box for reward points
        self.reward_input = QDoubleSpinBox(self)
        self.reward_input.setRange(-1000.00, 1000.00)  # set minimum and maximum values
        self.reward_input.setDecimals(2)  # set the number of decimal places
        self.reward_input.setSingleStep(0.01)  # set the step size

        # set up the form layout and add rows for inputs
        form_layout = QFormLayout()
        form_layout.addRow("Behaviour Points:", self.behaviour_input)
        form_layout.addRow("Reward Points:", self.reward_string_input)

        # set up button box for dialog controls
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)  # connect the accepted signal to accept method
        self.button_box.rejected.connect(self.reject)  # connect the rejected signal to reject method

        # set up the main layout for the dialog
        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)  # set the dialog's layout

    def get_data(self):
        """
        Return the current values of behaviour and reward points.

        :return: A tuple containing the behaviour points value and the reward points value.
        """
        return self.behaviour_input.value(), self.reward_input.value()
