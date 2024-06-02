from PyQt5.QtWidgets import QDialog, QDoubleSpinBox, QFormLayout, QVBoxLayout, QDialogButtonBox

class ChangePointsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Change Points")

        self.behaviour_input = QDoubleSpinBox(self)
        self.behaviour_input.setRange(-1000.00, 1000.00)
        self.behaviour_input.setDecimals(2)
        self.behaviour_input.setSingleStep(0.01)

        self.reward_input = QDoubleSpinBox(self)
        self.reward_input.setRange(-1000.00, 1000.00)
        self.reward_input.setDecimals(2)
        self.reward_input.setSingleStep(0.01)

        form_layout = QFormLayout()
        form_layout.addRow("Behaviour Points:", self.behaviour_input)
        form_layout.addRow("Reward Points:", self.reward_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.behaviour_input.value(), self.reward_input.value()
