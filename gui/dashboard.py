from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Dashboard(QWidget):
    """Dashboard widget for the NeuroFence desktop application."""

    status_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.selected_model_path = ""
        self._build_ui()
        self._log("NeuroFence Started")
        self._log("Waiting for model...")

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        title = QLabel("NeuroFence Dashboard")
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        main_layout.addWidget(title)

        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("Upload Model")
        self.load_button = QPushButton("Load Model")

        self.upload_button.clicked.connect(self.select_model_folder)

        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.load_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        info_group = QGroupBox("Model Information")
        info_layout = QGridLayout()

        self.labels = {}

        fields = [
            "Model Name",
            "Architecture",
            "Layers",
            "Hidden Size",
            "Parameters",
            "Vocabulary Size",
        ]

        for row, field in enumerate(fields):
            name = QLabel(f"{field}:")
            value = QLabel("N/A")
            info_layout.addWidget(name, row, 0)
            info_layout.addWidget(value, row, 1)
            self.labels[field] = value

        info_group.setLayout(info_layout)
        main_layout.addWidget(info_group)

        log_group = QGroupBox("Console Log")
        log_layout = QVBoxLayout()

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        log_layout.addWidget(self.console)
        log_group.setLayout(log_layout)

        main_layout.addWidget(log_group)

    def _log(self, message: str):
        self.console.append(message)

    def select_model_folder(self):
        self.status_changed.emit("Selecting Model...")

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Hugging Face Model Folder",
        )

        if not folder:
            self.status_changed.emit("Ready")
            self._log("Model selection cancelled.")
            return

        self.selected_model_path = folder

        self._log("")
        self._log("Model folder selected.")
        self._log(folder)
        self._log("Ready to load model.")

        self.status_changed.emit("Model Selected")
        self.status_changed.emit("Waiting for Scan")