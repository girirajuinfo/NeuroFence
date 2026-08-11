"""
gui/dashboard.py

NeuroFence - Enterprise Security Dashboard (PyQt6)

Pure GUI layer. Backend logic, signals and method names are unchanged.
"""

from datetime import datetime

from PyQt6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    QRectF,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


# ==========================================================
# Design tokens
# ==========================================================

BG_BASE = "#0B0F17"
BG_PANEL = "#121826"
BG_ELEVATED = "#182031"
BORDER = "#232C41"
TEXT = "#E6EBF5"
TEXT_MUTED = "#8A97B1"
ACCENT = "#3B82F6"
ACCENT_DIM = "#1E3A8A"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"
INFO = "#38BDF8"


STYLESHEET = f"""
QWidget {{
    background-color: {BG_BASE};
    color: {TEXT};
    font-family: "Segoe UI", "Inter", "SF Pro Display", Arial, sans-serif;
    font-size: 13px;
}}

QScrollArea, QScrollArea > QWidget > QWidget {{
    background: transparent;
    border: none;
}}

QGroupBox {{
    background-color: {BG_PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    margin-top: 18px;
    padding: 18px 18px 16px 18px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    color: {TEXT_MUTED};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 2px;
    padding: 0 6px;
    color: {TEXT_MUTED};
}}

QLabel {{
    background: transparent;
}}

QPushButton {{
    background-color: {BG_ELEVATED};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 10px 18px;
    color: {TEXT};
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: #202B41;
    border-color: {ACCENT};
}}

QPushButton:pressed {{
    background-color: #162033;
}}

QPushButton:disabled {{
    color: #56607A;
    border-color: #1B2333;
    background-color: #121826;
}}

QPushButton#primary {{
    background-color: {ACCENT};
    border: 1px solid {ACCENT};
    color: #FFFFFF;
}}

QPushButton#primary:hover {{
    background-color: #2F6FE0;
}}

QPushButton#primary:disabled {{
    background-color: {ACCENT_DIM};
    border-color: {ACCENT_DIM};
    color: #93A6C8;
}}

QPushButton#danger {{
    background-color: transparent;
    border: 1px solid {DANGER};
    color: {DANGER};
}}

QPushButton#danger:hover {{
    background-color: rgba(239, 68, 68, 0.12);
}}

QPushButton#danger:disabled {{
    border-color: #4A2733;
    color: #7A4450;
}}

QProgressBar {{
    background-color: {BG_ELEVATED};
    border: 1px solid {BORDER};
    border-radius: 8px;
    height: 16px;
    text-align: center;
}}

QProgressBar::chunk {{
    border-radius: 7px;
    background-color: {ACCENT};
}}

QTextEdit {{
    background-color: #080C14;
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 12px;
    font-family: "JetBrains Mono", "Cascadia Mono", Consolas, monospace;
    font-size: 12px;
    selection-background-color: {ACCENT_DIM};
}}

QTableWidget {{
    background-color: #0E1522;
    alternate-background-color: #121A29;
    border: 1px solid {BORDER};
    border-radius: 12px;
    gridline-color: #1B2434;
    selection-background-color: {ACCENT_DIM};
}}

QTableWidget::item {{
    padding: 8px 10px;
    border: none;
}}

QHeaderView::section {{
    background-color: {BG_ELEVATED};
    color: {TEXT_MUTED};
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 10px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QTableCornerButton::section {{
    background-color: {BG_ELEVATED};
    border: none;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 4px;
}}

QScrollBar::handle:vertical {{
    background: #2A3550;
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: #3A4A6E;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 4px;
}}

QScrollBar::handle:horizontal {{
    background: #2A3550;
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""


# ==========================================================
# Circular risk gauge
# ==========================================================

class RiskGauge(QWidget):
    """Animated circular risk gauge."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0.0
        self._label = "IDLE"
        self._color = QColor(ACCENT)
        self.setMinimumSize(210, 210)
        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed,
        )

        self._animation = QPropertyAnimation(self, b"value", self)
        self._animation.setDuration(900)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = float(value)
        self.update()

    value = pyqtProperty(float, fget=get_value, fset=set_value)

    def set_score(self, score, label, color):
        """Animate towards a new score."""
        self._label = label
        self._color = QColor(color)
        self._animation.stop()
        self._animation.setStartValue(self._value)
        self._animation.setEndValue(float(score))
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        side = min(self.width(), self.height())
        margin = 14
        rect = QRectF(
            (self.width() - side) / 2 + margin,
            (self.height() - side) / 2 + margin,
            side - 2 * margin,
            side - 2 * margin,
        )

        track_pen = QPen(QColor("#1C2436"))
        track_pen.setWidth(16)
        track_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(track_pen)
        painter.drawArc(rect, 0, 360 * 16)

        arc_pen = QPen(self._color)
        arc_pen.setWidth(16)
        arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(arc_pen)
        span = int(-self._value / 100.0 * 360 * 16)
        painter.drawArc(rect, 90 * 16, span)

        painter.setPen(QColor(TEXT))
        value_font = QFont(self.font())
        value_font.setPointSize(30)
        value_font.setBold(True)
        painter.setFont(value_font)
        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            f"{int(round(self._value))}%",
        )

        painter.setPen(self._color)
        label_font = QFont(self.font())
        label_font.setPointSize(10)
        label_font.setBold(True)
        painter.setFont(label_font)
        label_rect = QRectF(
            rect.x(),
            rect.y() + rect.height() * 0.62,
            rect.width(),
            rect.height() * 0.25,
        )
        painter.drawText(
            label_rect,
            Qt.AlignmentFlag.AlignCenter,
            self._label,
        )

        painter.end()


# ==========================================================
# Metric card
# ==========================================================

class MetricCard(QFrame):
    """Compact KPI card used in the dashboard summary strip."""

    def __init__(self, title, value="—", accent=ACCENT, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {BG_PANEL};
                border: 1px solid {BORDER};
                border-radius: 14px;
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(8)

        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet(
            f"color:{TEXT_MUTED}; font-size:11px;"
            "font-weight:700; letter-spacing:1px; border:none;"
        )

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            f"color:{TEXT}; font-size:24px; font-weight:700; border:none;"
        )

        self.accent_bar = QFrame()
        self.accent_bar.setFixedHeight(3)
        self.accent_bar.setStyleSheet(
            f"background-color:{accent}; border:none; border-radius:2px;"
        )

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.accent_bar)

    def set_value(self, text):
        self.value_label.setText(str(text))

    def set_accent(self, color):
        self.accent_bar.setStyleSheet(
            f"background-color:{color}; border:none; border-radius:2px;"
        )


# ==========================================================
# Dashboard
# ==========================================================

class Dashboard(QWidget):
    """Dashboard widget for the NeuroFence desktop application."""

    status_changed = pyqtSignal(str)

    # Signals consumed by app.py to drive the backend pipeline
    model_selected = pyqtSignal(str)
    scan_requested = pyqtSignal()
    stop_requested = pyqtSignal()
    export_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.selected_model_path = ""
        self._build_ui()
        self._log("NeuroFence Started")
        self._log("Waiting for model...")

    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    def _build_ui(self):
        self.setStyleSheet(STYLESHEET)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._build_toolbar())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        content_layout = QVBoxLayout(container)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(20)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # ---- header -------------------------------------
        header = QVBoxLayout()
        header.setSpacing(4)

        title = QLabel("Threat Analysis Dashboard")
        title.setStyleSheet(
            f"font-size:22px; font-weight:700; color:{TEXT};"
        )

        subtitle = QLabel(
            "Offline LLM weight poisoning and backdoor detection"
        )
        subtitle.setStyleSheet(f"font-size:13px; color:{TEXT_MUTED};")

        header.addWidget(title)
        header.addWidget(subtitle)
        content_layout.addLayout(header)

        # ---- KPI strip ----------------------------------
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(16)

        self.card_status = MetricCard("Scan Status", "Idle", ACCENT)
        self.card_layers = MetricCard("Captured Layers", "0", INFO)
        self.card_spikes = MetricCard("Activation Spikes", "0", WARNING)
        self.card_dormant = MetricCard("Dormant Neurons", "0", DANGER)

        for card in (
            self.card_status,
            self.card_layers,
            self.card_spikes,
            self.card_dormant,
        ):
            kpi_row.addWidget(card)

        content_layout.addLayout(kpi_row)

        # ---- risk + progress row ------------------------
        upper_row = QHBoxLayout()
        upper_row.setSpacing(20)

        upper_row.addWidget(self._build_risk_group(), 1)
        upper_row.addWidget(self._build_progress_group(), 2)

        content_layout.addLayout(upper_row)

        # ---- model info + statistics --------------------
        mid_row = QHBoxLayout()
        mid_row.setSpacing(20)

        mid_row.addWidget(self._build_model_group(), 1)
        mid_row.addWidget(self._build_stats_group(), 1)

        content_layout.addLayout(mid_row)

        # ---- activation table ---------------------------
        content_layout.addWidget(self._build_activation_group())

        # ---- history + console --------------------------
        lower_row = QHBoxLayout()
        lower_row.setSpacing(20)

        lower_row.addWidget(self._build_history_group(), 1)
        lower_row.addWidget(self._build_console_group(), 1)

        content_layout.addLayout(lower_row)
        content_layout.addStretch()

    # ---- toolbar ----------------------------------------

    def _build_toolbar(self):
        bar = QFrame()
        bar.setStyleSheet(
            f"""
            QFrame {{
                background-color: {BG_PANEL};
                border-bottom: 1px solid {BORDER};
            }}
            """
        )

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 14, 24, 14)
        layout.setSpacing(10)

        self.upload_button = QPushButton("⬆  Upload Model")
        self.load_button = QPushButton("⟳  Load Model")
        self.start_scan_button = QPushButton("▶  Start Scan")
        self.start_scan_button.setObjectName("primary")
        self.start_scan_button.setEnabled(False)

        self.stop_scan_button = QPushButton("■  Stop Scan")
        self.stop_scan_button.setObjectName("danger")
        self.stop_scan_button.clicked.connect(self.stop_scan)
        self.stop_scan_button.setEnabled(False)

        self.clear_button = QPushButton("⌫  Clear Console")

        self.export_button = QPushButton("⇩  Export Report")
        self.export_button.setEnabled(False)

        self.upload_button.clicked.connect(self.select_model_folder)
        self.load_button.clicked.connect(self.select_model_folder)
        self.start_scan_button.clicked.connect(self.start_scan)
        self.export_button.clicked.connect(self.export_requested.emit)

        for button in (
            self.upload_button,
            self.load_button,
            self.start_scan_button,
            self.stop_scan_button,
            self.clear_button,
            self.export_button,
        ):
            layout.addWidget(button)

        layout.addStretch()

        self.model_path_label = QLabel("No model selected")
        self.model_path_label.setStyleSheet(
            f"color:{TEXT_MUTED}; font-size:12px; border:none;"
        )
        layout.addWidget(self.model_path_label)

        return bar

    # ---- risk -------------------------------------------

    def _build_risk_group(self):
        risk_group = QGroupBox("AI SECURITY SCORE")
        risk_layout = QVBoxLayout()
        risk_layout.setSpacing(12)

        self.risk_gauge = RiskGauge()

        gauge_row = QHBoxLayout()
        gauge_row.addStretch()
        gauge_row.addWidget(self.risk_gauge)
        gauge_row.addStretch()

        self.risk_score = QLabel("0%")
        self.risk_score.setStyleSheet(
            f"font-size:20px; font-weight:700; color:{TEXT};"
        )

        self.risk_status = QLabel("AWAITING SCAN")
        self.risk_status.setStyleSheet(
            f"font-size:12px; font-weight:700; letter-spacing:1px;"
            f"color:{TEXT_MUTED};"
        )

        risk_layout.addLayout(gauge_row)
        risk_layout.addWidget(self.risk_score)
        risk_layout.addWidget(self.risk_status)
        risk_layout.setAlignment(
            self.risk_score, Qt.AlignmentFlag.AlignCenter
        )
        risk_layout.setAlignment(
            self.risk_status, Qt.AlignmentFlag.AlignCenter
        )

        risk_group.setLayout(risk_layout)
        return risk_group

    # ---- progress ---------------------------------------

    def _build_progress_group(self):
        progress_group = QGroupBox("SCAN PROGRESS")
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(14)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(18)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(0)

        self._progress_animation = QPropertyAnimation(
            self.progress_bar, b"value", self
        )
        self._progress_animation.setDuration(500)
        self._progress_animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet(
            f"font-size:34px; font-weight:700; color:{TEXT};"
        )

        self.prompt_label = QLabel("Prompt: 0 / 200")
        self.prompt_label.setStyleSheet(f"color:{TEXT_MUTED};")

        self.remaining_label = QLabel("Remaining: 00:00:00")
        self.remaining_label.setStyleSheet(f"color:{TEXT_MUTED};")

        meta_row = QHBoxLayout()
        meta_row.addWidget(self.prompt_label)
        meta_row.addStretch()
        meta_row.addWidget(self.remaining_label)

        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(meta_row)

        pipeline = QLabel(
            "Pipeline:  Upload → Load → Metadata → Scan → Prompts → "
            "Activations → Detection → Risk → JSON → PDF"
        )
        pipeline.setWordWrap(True)
        pipeline.setStyleSheet(
            f"color:{TEXT_MUTED}; font-size:11px; letter-spacing:0.5px;"
        )
        progress_layout.addWidget(pipeline)
        progress_layout.addStretch()

        progress_group.setLayout(progress_layout)
        return progress_group

    # ---- model info -------------------------------------

    def _build_model_group(self):
        info_group = QGroupBox("MODEL INFORMATION")
        info_layout = QGridLayout()
        info_layout.setVerticalSpacing(12)
        info_layout.setHorizontalSpacing(18)
        info_layout.setColumnStretch(1, 1)

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
            name = QLabel(field.upper())
            name.setStyleSheet(
                f"color:{TEXT_MUTED}; font-size:11px;"
                "font-weight:600; letter-spacing:0.6px;"
            )

            value = QLabel("N/A")
            value.setStyleSheet(
                f"color:{TEXT}; font-size:13px; font-weight:600;"
            )
            value.setAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            info_layout.addWidget(name, row, 0)
            info_layout.addWidget(value, row, 1)

            self.labels[field] = value

        info_group.setLayout(info_layout)
        return info_group

    # ---- statistics -------------------------------------

    def _build_stats_group(self):
        stats_group = QGroupBox("SCAN STATISTICS")
        stats_layout = QGridLayout()
        stats_layout.setVerticalSpacing(12)
        stats_layout.setHorizontalSpacing(18)
        stats_layout.setColumnStretch(1, 1)

        captions = [
            "Total Prompts",
            "Completed",
            "Remaining",
            "Execution Time",
            "Average Time",
            "Memory Usage",
        ]

        for row, caption in enumerate(captions):
            label = QLabel(caption.upper())
            label.setStyleSheet(
                f"color:{TEXT_MUTED}; font-size:11px;"
                "font-weight:600; letter-spacing:0.6px;"
            )
            stats_layout.addWidget(label, row, 0)

        self.total_prompts = QLabel("200")
        self.completed = QLabel("0")
        self.remaining = QLabel("200")
        self.execution = QLabel("00:00:00")
        self.average = QLabel("0 sec")
        self.memory = QLabel("0 MB")

        values = [
            self.total_prompts,
            self.completed,
            self.remaining,
            self.execution,
            self.average,
            self.memory,
        ]

        for row, value in enumerate(values):
            value.setStyleSheet(
                f"color:{TEXT}; font-size:13px; font-weight:600;"
            )
            value.setAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )
            stats_layout.addWidget(value, row, 1)

        stats_group.setLayout(stats_layout)
        return stats_group

    # ---- activation table -------------------------------

    def _build_activation_group(self):
        activation_group = QGroupBox("ACTIVATION SUMMARY")
        activation_layout = QVBoxLayout()

        self.activation_table = QTableWidget()
        self.activation_table.setColumnCount(4)
        self.activation_table.setRowCount(4)
        self.activation_table.setMinimumHeight(220)
        self.activation_table.verticalHeader().setVisible(False)
        self.activation_table.verticalHeader().setDefaultSectionSize(38)

        self.activation_table.setHorizontalHeaderLabels(
            ["Layer", "Mean Activation", "Max Activation", "Status"]
        )

        self.activation_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.activation_table.horizontalHeader().setStretchLastSection(True)
        self.activation_table.setAlternatingRowColors(True)
        self.activation_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.activation_table.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection
        )
        self.activation_table.setShowGrid(False)

        dummy_data = [
            ("Layer 1", "0.021", "0.95", "Normal"),
            ("Layer 2", "0.034", "1.10", "Normal"),
            ("Layer 3", "0.052", "1.42", "Warning"),
            ("Layer 4", "0.023", "1.23", "Normal"),
        ]

        for row, data in enumerate(dummy_data):
            self._set_activation_row(row, data)

        activation_layout.addWidget(self.activation_table)
        activation_group.setLayout(activation_layout)
        return activation_group

    def _set_activation_row(self, row, data):
        """Populate one activation row with status colouring."""
        status_colors = {
            "normal": SUCCESS,
            "warning": WARNING,
            "critical": DANGER,
            "anomaly": DANGER,
        }

        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))

            if col == 0:
                item.setForeground(QColor(TEXT))
            elif col == 3:
                item.setForeground(
                    QColor(
                        status_colors.get(str(value).lower(), TEXT_MUTED)
                    )
                )
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            else:
                item.setForeground(QColor(TEXT_MUTED))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

            self.activation_table.setItem(row, col, item)

    # ---- scan history -----------------------------------

    def _build_history_group(self):
        history_group = QGroupBox("SCAN HISTORY")
        history_layout = QVBoxLayout()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setRowCount(0)
        self.history_table.setMinimumHeight(220)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.verticalHeader().setDefaultSectionSize(36)
        self.history_table.setHorizontalHeaderLabels(
            ["Timestamp", "Model", "Risk", "Result"]
        )
        self.history_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setShowGrid(False)
        self.history_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.history_table.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection
        )

        history_layout.addWidget(self.history_table)
        history_group.setLayout(history_layout)
        return history_group

    def _add_history_entry(self, model_name, risk, result, color=SUCCESS):
        """Insert a new row at the top of the scan history table."""
        self.history_table.insertRow(0)

        values = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            model_name,
            str(risk),
            result,
        ]

        for col, value in enumerate(values):
            item = QTableWidgetItem(value)
            if col == 3:
                item.setForeground(QColor(color))
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            else:
                item.setForeground(QColor(TEXT_MUTED))
            self.history_table.setItem(0, col, item)

    # ---- console ----------------------------------------

    def _build_console_group(self):
        log_group = QGroupBox("CONSOLE LOG")
        log_layout = QVBoxLayout()

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(220)
        self.console.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.clear_button.clicked.connect(self.console.clear)

        log_layout.addWidget(self.console)
        log_group.setLayout(log_layout)
        return log_group

    # ------------------------------------------------------
    # Logging
    # ------------------------------------------------------

    def _log(self, message: str, level="INFO"):

        current_time = datetime.now().strftime("%H:%M:%S")

        colors = {
            "INFO": INFO,
            "SUCCESS": SUCCESS,
            "WARNING": WARNING,
            "ERROR": DANGER,
        }

        color = colors.get(level, TEXT_MUTED)

        self.console.append(
            f'<span style="color:{TEXT_MUTED};">[{current_time}]</span> '
            f'<span style="color:{color};font-weight:600;">[{level}]</span> '
            f'<span style="color:{TEXT};">{message}</span>'
        )

        self.console.verticalScrollBar().setValue(
            self.console.verticalScrollBar().maximum()
        )

    def _set_progress(self, percent):
        """Animate the progress bar to a percentage."""
        self._progress_animation.stop()
        self._progress_animation.setStartValue(self.progress_bar.value())
        self._progress_animation.setEndValue(int(percent))
        self._progress_animation.start()
        self.progress_label.setText(f"{int(percent)}%")

    def _set_risk(self, score, status, color):
        """Update gauge and risk labels."""
        self.risk_gauge.set_score(score, status, color)
        self.risk_score.setText(f"{score}%")
        self.risk_status.setText(status)
        self.risk_score.setStyleSheet(
            f"font-size:20px; font-weight:700; color:{color};"
        )
        self.risk_status.setStyleSheet(
            f"font-size:12px; font-weight:700; letter-spacing:1px;"
            f"color:{color};"
        )

    # ------------------------------------------------------
    # Backend-facing actions (unchanged behaviour)
    # ------------------------------------------------------

    def select_model_folder(self):
        """Pick a model folder and hand it to the backend (app.py)."""

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
        self.model_path_label.setText(folder)

        self._log(f"Selected model folder: {folder}", "INFO")

        self.card_status.set_value("Loading")
        self.card_status.set_accent(INFO)

        self.start_scan_button.setEnabled(False)
        self.export_button.setEnabled(False)

        self.status_changed.emit("Loading Model...")

        # Backend work happens in app.py
        self.model_selected.emit(folder)

    def start_scan(self):
        """Ask the backend (app.py) to run the full pipeline."""

        if not self.selected_model_path:
            self._log("No model selected.", "WARNING")
            return

        self.status_changed.emit("Scanning...")

        self.upload_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.start_scan_button.setEnabled(False)
        self.stop_scan_button.setEnabled(True)
        self.export_button.setEnabled(False)

        self.card_status.set_value("Scanning")
        self.card_status.set_accent(WARNING)

        self._set_progress(0)
        self.completed.setText("0")
        self.execution.setText("00:00:00")

        self.scan_requested.emit()

    def stop_scan(self):
        """Request a safe stop, then reset the scan indicators."""

        self.stop_requested.emit()

        self._log("Scan Stopped", "WARNING")

        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")
        self.prompt_label.setText("Prompt: 0 / 0")
        self.remaining_label.setText("Remaining: 00:00:00")

        self.completed.setText("0")
        self.execution.setText("00:00:00")
        self.average.setText("0 sec")
        self.memory.setText("0 MB")

        self._set_risk(0, "SCAN STOPPED", WARNING)

        self.card_status.set_value("Stopped")
        self.card_status.set_accent(WARNING)

        self.upload_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.start_scan_button.setEnabled(
            bool(self.selected_model_path)
        )
        self.stop_scan_button.setEnabled(False)

        self.status_changed.emit("Scan Stopped")

    # ------------------------------------------------------
    # Public API used by app.py (no GUI redesign)
    # ------------------------------------------------------

    def log(self, message, level="INFO"):
        """Public logging entry point for backend messages."""
        self._log(message, level)

    def set_stage(self, stage, percent):
        """Update the progress bar and console for a pipeline stage."""
        self._set_progress(percent)
        self.status_changed.emit(stage)

    def show_metadata(self, metadata):
        """Display real backend metadata on the dashboard."""

        def text(key, default="N/A"):
            value = metadata.get(key, default)
            return "N/A" if value is None else str(value)

        parameters = metadata.get("total_parameters")

        if isinstance(parameters, (int, float)):
            if parameters >= 1_000_000_000:
                parameters_text = f"{parameters / 1_000_000_000:.2f} B"
            elif parameters >= 1_000_000:
                parameters_text = f"{parameters / 1_000_000:.2f} M"
            else:
                parameters_text = f"{parameters:,}"
        else:
            parameters_text = "N/A"

        self.labels["Model Name"].setText(text("model_name"))
        self.labels["Architecture"].setText(text("architecture"))
        self.labels["Layers"].setText(text("num_layers"))
        self.labels["Hidden Size"].setText(text("hidden_size"))
        self.labels["Parameters"].setText(parameters_text)
        self.labels["Vocabulary Size"].setText(text("vocab_size"))
        self.labels["Device"].setText(text("device", "CPU"))
        self.labels["Model Size"].setText(text("model_size"))

        self.card_status.set_value("Ready")
        self.card_status.set_accent(INFO)

        self.status_changed.emit("Model Loaded")

    def set_prompt_count(self, count):
        """Show how many prompts the backend loaded."""
        self.total_prompts.setText(str(count))
        self.remaining.setText(str(count))
        self.prompt_label.setText(f"Prompt: 0 / {count}")

    def enable_scan(self, enabled=True):
        """Enable or disable the Start Scan button."""
        self.start_scan_button.setEnabled(bool(enabled))
        self.upload_button.setEnabled(True)
        self.load_button.setEnabled(True)

    def show_activation_statistics(self, statistics, limit=12):
        """Fill the activation table with real layer statistics."""

        items = list(statistics.items())

        items.sort(
            key=lambda entry: entry[1].get("spikes", 0),
            reverse=True,
        )

        items = items[:limit]

        self.activation_table.setRowCount(len(items))

        for row, (layer_name, stats) in enumerate(items):
            spikes = stats.get("spikes", 0)

            if spikes > 25:
                status = "Critical"
            elif spikes > 0:
                status = "Warning"
            else:
                status = "Normal"

            self._set_activation_row(
                row,
                (
                    layer_name,
                    f"{stats.get('mean', 0.0):.4f}",
                    f"{stats.get('std', 0.0):.4f}",
                    status,
                ),
            )

    def show_scan_results(self, results):
        """Render the complete backend result payload."""

        summary = results.get("scan_summary", {}) or {}
        metadata = results.get("metadata", {}) or {}
        statistics = results.get("statistics", {}) or {}

        captured_layers = results.get(
            "activation_summary", {}
        ).get("captured_layers", len(statistics))

        prompt_count = results.get("prompt_count", 0)
        execution_time = float(results.get("execution_time", 0.0))

        risk_level = str(summary.get("risk_level", "UNKNOWN"))
        risk_score = summary.get("risk_score", 0)

        colors = {
            "safe": SUCCESS,
            "low": SUCCESS,
            "medium": WARNING,
            "high": DANGER,
            "critical": DANGER,
        }

        color = colors.get(risk_level.lower(), INFO)

        gauge_value = max(0, min(100, int(risk_score)))

        self._set_risk(gauge_value, risk_level.upper(), color)
        self.risk_score.setText(f"{risk_score}")

        self.card_status.set_value("Complete")
        self.card_status.set_accent(SUCCESS)
        self.card_layers.set_value(str(captured_layers))
        self.card_spikes.set_value(str(summary.get("total_spikes", 0)))
        self.card_dormant.set_value(
            str(summary.get("total_dormant_neurons", 0))
        )

        self.show_activation_statistics(statistics)

        hours, remainder = divmod(int(execution_time), 3600)
        minutes, seconds = divmod(remainder, 60)

        self.total_prompts.setText(str(prompt_count))
        self.completed.setText(str(prompt_count))
        self.remaining.setText("0")
        self.execution.setText(
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )
        self.average.setText(
            f"{execution_time / prompt_count:.2f} sec"
            if prompt_count else "0 sec"
        )
        self.prompt_label.setText(
            f"Prompt: {prompt_count} / {prompt_count}"
        )
        self.remaining_label.setText("Remaining: 00:00:00")

        self._set_progress(100)

        self._add_history_entry(
            metadata.get("model_name", "Unknown"),
            str(risk_score),
            risk_level.upper(),
            color,
        )

        self._log("Scan Completed Successfully", "SUCCESS")

        self.upload_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.start_scan_button.setEnabled(True)
        self.stop_scan_button.setEnabled(False)
        self.export_button.setEnabled(True)

        self.status_changed.emit("Scan Completed Successfully")

    def scan_failed(self, message):
        """Report a backend failure without crashing the GUI."""

        self._log(f"Scan failed: {message}", "ERROR")

        self.card_status.set_value("Failed")
        self.card_status.set_accent(DANGER)

        self._set_risk(0, "SCAN FAILED", DANGER)

        self.upload_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.start_scan_button.setEnabled(
            bool(self.selected_model_path)
        )
        self.stop_scan_button.setEnabled(False)

        self.status_changed.emit("Scan Failed")

    def set_memory_usage(self, text):
        """Display memory usage reported by the backend."""
        self.memory.setText(text)