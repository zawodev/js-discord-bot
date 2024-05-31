from PyQt5.QtWidgets import QDialog, QSpinBox, QFormLayout, QVBoxLayout, QDialogButtonBox

class ChangePointsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change User Points")

        # SpinBox for behavioural points
        self.behaviour_points_input = QSpinBox(self)
        self.behaviour_points_input.setRange(-1000, 1000)

        # SpinBox for reward points
        self.reward_points_input = QSpinBox(self)
        self.reward_points_input.setRange(-1000, 1000)

        form_layout = QFormLayout()
        form_layout.addRow("Behaviour Points:", self.behaviour_points_input)
        form_layout.addRow("Reward Points:", self.reward_points_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.behaviour_points_input.value(), self.reward_points_input.value()
