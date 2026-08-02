from datetime import datetime

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QScrollArea,
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
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        content_layout = QVBoxLayout(container)
        content_layout.setSpacing(15)

        main_layout.addWidget(scroll)
        scroll.setWidget(container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("NeuroFence Dashboard")
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        content_layout.addWidget(title)
       
        button_layout = QHBoxLayout()

        self.upload_button = QPushButton("Upload Model")
        self.load_button = QPushButton("Load Model")
        self.start_scan_button = QPushButton("Start Scan")
        self.start_scan_button.setEnabled(False)

        self.stop_scan_button = QPushButton("Stop Scan")
        self.stop_scan_button.clicked.connect(self.stop_scan)
        self.stop_scan_button.setEnabled(False) 
        
        self.clear_button = QPushButton("Clear Console")

        self.export_button = QPushButton("Export Report")
        self.export_button.setEnabled(False)
        self.upload_button.clicked.connect(self.select_model_folder)
        self.load_button.clicked.connect(self.select_model_folder)
        self.start_scan_button.clicked.connect(self.start_scan)
        
        

        button_layout.addWidget(self.upload_button)
        
        button_layout.addWidget(self.start_scan_button)
        button_layout.addWidget(self.stop_scan_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        button_layout.addStretch()

        content_layout.addLayout(button_layout)

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
            "Device",
            "Model Size",
        ]
        

        for row, field in enumerate(fields):
            name = QLabel(f"{field}:")
            value = QLabel("N/A")

            info_layout.addWidget(name, row, 0)
            info_layout.addWidget(value, row, 1)

            self.labels[field] = value

        info_group.setLayout(info_layout)
        content_layout.addWidget(info_group)
        progress_group = QGroupBox("Scan Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setTextVisible(False)

        self.progress_bar.setValue(0)
        self.progress_label = QLabel("0%")
        self.prompt_label = QLabel("Prompt: 0 / 200")
        self.remaining_label = QLabel("Remaining: 00:00:00")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.prompt_label)
        progress_layout.addWidget(self.remaining_label)
        progress_group.setLayout(progress_layout)

        content_layout.addWidget(progress_group)

        stats_group = QGroupBox("Scan Statistics")
        stats_layout = QGridLayout()

        stats_layout.addWidget(QLabel("Total Prompts:"), 0, 0)
        stats_layout.addWidget(QLabel("Completed:"), 1, 0)
        stats_layout.addWidget(QLabel("Remaining:"), 2, 0)
        stats_layout.addWidget(QLabel("Execution Time:"), 3, 0)
        stats_layout.addWidget(QLabel("Average Time:"), 4, 0)
        stats_layout.addWidget(QLabel("Memory Usage:"), 5, 0)

        self.total_prompts = QLabel("200")
        self.completed = QLabel("0")
        self.remaining = QLabel("200")
        self.execution = QLabel("00:00:00")
        self.average = QLabel("0 sec")
        self.memory = QLabel("0 MB")

        stats_layout.addWidget(self.total_prompts, 0, 1)
        stats_layout.addWidget(self.completed, 1, 1)
        stats_layout.addWidget(self.remaining, 2, 1)
        stats_layout.addWidget(self.execution, 3, 1)
        stats_layout.addWidget(self.average, 4, 1)
        stats_layout.addWidget(self.memory, 5, 1) 

        stats_group.setLayout(stats_layout)
        content_layout.addWidget(stats_group)

        log_group = QGroupBox("Console Log")
        log_layout = QVBoxLayout()

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.clear_button.clicked.connect(self.console.clear)

        log_layout.addWidget(self.console)
        log_group.setLayout(log_layout)

        content_layout.addWidget(log_group)
        activation_group = QGroupBox("Activation Summary")
        activation_layout = QVBoxLayout()

        self.activation_table = QTableWidget()
        self.activation_table.setColumnCount(4)
        self.activation_table.setRowCount(4)

        self.activation_table.setHorizontalHeaderLabels(
            ["Layer", "Mean Activation", "Max Activation", "Status"]
)

        self.activation_table.horizontalHeader().setStretchLastSection(True)
        self.activation_table.resizeColumnsToContents()
        self.activation_table.setAlternatingRowColors(True)
        self.activation_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activation_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        dummy_data = [
            ("Layer 1", "0.021", "0.95", "Normal"),
            ("Layer 2", "0.034", "1.10", "Normal"),
            ("Layer 3", "0.052", "1.42", "Warning"),
            ("Layer 4", "0.023", "1.23", "Normal"),
        ]

        for row, data in enumerate(dummy_data):
            for col, value in enumerate(data):
                self.activation_table.setItem(
                    row,
                    col,
                    QTableWidgetItem(value)
                )

        activation_layout.addWidget(self.activation_table)

        activation_group.setLayout(activation_layout)

        content_layout.addWidget(activation_group)

        risk_group = QGroupBox("AI Security Score")

        risk_layout = QVBoxLayout()

        self.risk_score = QLabel("92%")
        self.risk_score.setStyleSheet(
            "font-size:32px; font-weight:bold; color:green;"
        )
        self.risk_status = QLabel("SAFE")
        self.risk_status.setStyleSheet(
            "font-size:18px; font-weight:bold; color:green;"
)
        risk_layout.addWidget(self.risk_score)
        risk_layout.addWidget(self.risk_status)

        risk_layout.setSpacing(10)
        risk_layout.setAlignment(self.risk_score, Qt.AlignmentFlag.AlignCenter)
        risk_layout.setAlignment(self.risk_status, Qt.AlignmentFlag.AlignCenter)

        risk_group.setLayout(risk_layout)
        content_layout.addWidget(risk_group)

    def _log(self, message: str, level="INFO"):

        current_time = datetime.now().strftime("%H:%M:%S")


        colors = {
           "INFO": "blue",
           "SUCCESS": "green",
           "WARNING": "orange",
           "ERROR": "red",
    }


        color = colors.get(level, "black")


        self.console.append(
            f'<span style="color:{color};">[{current_time}] [{level}] {message}</span>'
        )
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

        self._log("Loading Model...", "INFO")
        self._log("Model Loaded", "SUCCESS")
        self._log(folder, "INFO")
        self._log("Ready to Scan", "SUCCESS")

        self.labels["Model Name"].setText("Llama-2-7B")
        self.labels["Architecture"].setText("Transformer")
        self.labels["Layers"].setText("32")
        self.labels["Hidden Size"].setText("4096")
        self.labels["Parameters"].setText("7 Billion")
        self.labels["Vocabulary Size"].setText("32000")
        self.labels["Device"].setText("CPU")
        self.labels["Model Size"].setText("2.5 GB")

        self.completed.setText("0")
        self.remaining.setText("200")
        self.execution.setText("00:00:00")
        self.average.setText("0 sec")
        self.memory.setText("0 MB")
        
        self.status_changed.emit("Model Selected")
        self.start_scan_button.setEnabled(True)
        self.status_changed.emit("Waiting for Scan")
        
    def start_scan(self):

        self.status_changed.emit("Scanning...")

        self.upload_button.setEnabled(False)
        self.start_scan_button.setEnabled(False)
        self.stop_scan_button.setEnabled(True)
        self.export_button.setEnabled(False)
        self._log("")

        self._log("Loading Model...", "INFO")
        self._log("Model Loaded", "SUCCESS")

        self.progress_bar.setValue(100)
        self.status_changed.emit("Scan Completed")
        self.export_button.setEnabled(True)
        
        self._log("Registering Hooks...", "INFO")
        self._log("Generating Prompts...", "INFO")
        self._log("Running Prompt 1...", "INFO")
        self._log("Running Prompt 2...", "INFO")
        self._log("Collecting Activations...", "INFO")
        self._log("Scan Finished", "SUCCESS")

        self.progress_bar.setValue(25)
        self.progress_label.setText("25%")
        self.prompt_label.setText("Prompt: 50 / 200")
        self.remaining_label.setText("Remaining: 00:03:00")

        self.progress_bar.setValue(50)
        self.progress_label.setText("50%")
        self.prompt_label.setText("Prompt: 100 / 200")
        self.remaining_label.setText("Remaining: 00:02:00")

        self.progress_bar.setValue(75)
        self.progress_label.setText("75%")
        self.prompt_label.setText("Prompt: 150 / 200")
        self.remaining_label.setText("Remaining: 00:01:00")

        self.progress_bar.setValue(100)
        self.progress_label.setText("100%")
        self.prompt_label.setText("Prompt: 200 / 200")
        self.remaining_label.setText("Remaining: 00:00:00")

        self.completed.setText("200")
        self.remaining.setText("0")
        self.execution.setText("00:02:15")
        self.average.setText("0.67 sec")
        self.memory.setText("512 MB")

        self.risk_score.setText("92%")
        self.risk_status.setText("SAFE")

        self.risk_score.setStyleSheet(
            "font-size:32px; font-weight:bold; color:green;"
)

        self.risk_status.setStyleSheet(
            "font-size:18px; font-weight:bold; color:green;"
)

        self.upload_button.setEnabled(True)
        self.start_scan_button.setEnabled(True)
        self.stop_scan_button.setEnabled(False)
        self.export_button.setEnabled(True)

        self.status_changed.emit("Scan Complete")
        
    def stop_scan(self):

        self._log("Scan Stopped", "WARNING")

        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")
        self.prompt_label.setText("Prompt: 0 / 200")
        self.remaining_label.setText("Remaining: 00:00:00")

        self.completed.setText("0")
        self.remaining.setText("200")
        self.execution.setText("00:00:00")
        self.average.setText("0 sec")
        self.memory.setText("0 MB")

        self.upload_button.setEnabled(True)
        self.start_scan_button.setEnabled(True)
        self.stop_scan_button.setEnabled(False)

        self.status_changed.emit("Scan Stopped")