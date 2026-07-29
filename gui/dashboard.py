from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QGroupBox,
    QTextEdit,
    QSizePolicy,
)


class Dashboard(QWidget):
    """Main dashboard layout for the NeuroFence application."""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Buttons
        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("Upload Model")
        self.start_scan_button = QPushButton("Start Scan")

        self.upload_button.setMinimumHeight(40)
        self.start_scan_button.setMinimumHeight(40)

        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.start_scan_button)

        main_layout.addLayout(button_layout)

        # Model Information Panel
        model_group = QGroupBox("Model Information")
        model_layout = QVBoxLayout()

        self.model_info_label = QLabel(
            "No model loaded.\n\n"
            "Model Name: -\n"
            "File Size: -\n"
            "Model Type: -"
        )
        self.model_info_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        model_layout.addWidget(self.model_info_label)
        model_group.setLayout(model_layout)

        main_layout.addWidget(model_group)

        # Risk Score
        risk_group = QGroupBox("Risk Score")
        risk_layout = QVBoxLayout()

        self.risk_score_label = QLabel("Risk Score: N/A")
        self.risk_score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        risk_layout.addWidget(self.risk_score_label)
        risk_group.setLayout(risk_layout)

        main_layout.addWidget(risk_group)

        # Scan Log
        log_group = QGroupBox("Scan Log")
        log_layout = QVBoxLayout()

        self.scan_log = QTextEdit()
        self.scan_log.setReadOnly(True)
        self.scan_log.setPlaceholderText(
            "Scan log messages will appear here..."
        )
        self.scan_log.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        log_layout.addWidget(self.scan_log)
        log_group.setLayout(log_layout)

        main_layout.addWidget(log_group)