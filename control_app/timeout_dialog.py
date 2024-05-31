from PyQt5.QtWidgets import QDialog, QLineEdit, QSpinBox, QFormLayout, QVBoxLayout, QDialogButtonBox


class TimeoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Timeout User")

        self.reason_input = QLineEdit(self)
        self.duration_input = QSpinBox(self)
        self.duration_input.setMinimum(1)
        self.duration_input.setMaximum(999999)  # arbitrary large number

        form_layout = QFormLayout()
        form_layout.addRow("Reason:", self.reason_input)
        form_layout.addRow("Duration (seconds):", self.duration_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def get_data(self):
        return self.reason_input.text(), self.duration_input.value()
