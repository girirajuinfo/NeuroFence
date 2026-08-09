"""
gui/main_window.py

NeuroFence - Main application window (PyQt6)

Adds an enterprise navigation sidebar, toolbar and status bar around the
existing Dashboard widget. All backend signals and methods are preserved.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from dashboard import (
    ACCENT,
    BG_BASE,
    BG_ELEVATED,
    BG_PANEL,
    BORDER,
    SUCCESS,
    TEXT,
    TEXT_MUTED,
    Dashboard,
)


APP_STYLESHEET = f"""
QMainWindow {{
    background-color: {BG_BASE};
}}

QMenuBar {{
    background-color: {BG_PANEL};
    color: {TEXT};
    border-bottom: 1px solid {BORDER};
    padding: 4px 8px;
    font-size: 13px;
}}

QMenuBar::item {{
    background: transparent;
    padding: 6px 12px;
    border-radius: 6px;
}}

QMenuBar::item:selected {{
    background-color: {BG_ELEVATED};
}}

QMenu {{
    background-color: {BG_PANEL};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 6px;
}}

QMenu::item {{
    padding: 8px 22px;
    border-radius: 6px;
}}

QMenu::item:selected {{
    background-color: {BG_ELEVATED};
    color: {TEXT};
}}

QMenu::separator {{
    height: 1px;
    background: {BORDER};
    margin: 6px 8px;
}}

QStatusBar {{
    background-color: {BG_PANEL};
    color: {TEXT_MUTED};
    border-top: 1px solid {BORDER};
    font-size: 12px;
    padding: 4px 12px;
}}

QStatusBar::item {{
    border: none;
}}

QMessageBox {{
    background-color: {BG_PANEL};
    color: {TEXT};
}}
"""


SIDEBAR_STYLESHEET = f"""
QFrame#sidebar {{
    background-color: {BG_PANEL};
    border-right: 1px solid {BORDER};
}}

QLabel#brand {{
    color: {TEXT};
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

QLabel#brandSub {{
    color: {TEXT_MUTED};
    font-size: 11px;
    letter-spacing: 1.4px;
    font-weight: 600;
}}

QLabel#navSection {{
    color: {TEXT_MUTED};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
    padding-left: 6px;
}}

QPushButton#nav {{
    background: transparent;
    border: none;
    border-radius: 10px;
    color: {TEXT_MUTED};
    text-align: left;
    padding: 11px 14px;
    font-size: 13px;
    font-weight: 600;
}}

QPushButton#nav:hover {{
    background-color: {BG_ELEVATED};
    color: {TEXT};
}}

QPushButton#nav:checked {{
    background-color: rgba(59, 130, 246, 0.16);
    color: {TEXT};
    border-left: 3px solid {ACCENT};
}}
"""


class MainWindow(QMainWindow):
    """Main window for the NeuroFence application."""

    def __init__(self):
        super().__init__()
        self.dashboard = Dashboard()
        self.dashboard.start_scan_button.setEnabled(False)
        self._setup_ui()

    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    def _setup_ui(self):
        self.setWindowTitle("NeuroFence — AI Model Security Platform")
        self.resize(1500, 950)
        self.setMinimumSize(1180, 760)
        self.setStyleSheet(APP_STYLESHEET)

        icon_path = os.path.join("assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._create_sidebar())
        layout.addWidget(self.dashboard, 1)

        self.setCentralWidget(central)

        self._create_menu()
        self._create_status_bar()

        self.dashboard.status_changed.connect(
            self.statusBar().showMessage
        )
        self.dashboard.status_changed.connect(self._update_state_label)

    # ---- sidebar ----------------------------------------

    def _create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(248)
        sidebar.setStyleSheet(SIDEBAR_STYLESHEET)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 22, 16, 18)
        layout.setSpacing(6)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)

        mark = QLabel("◈")
        mark.setStyleSheet(
            f"color:{ACCENT}; font-size:24px; font-weight:700;"
        )

        brand_text = QVBoxLayout()
        brand_text.setSpacing(0)

        brand = QLabel("NeuroFence")
        brand.setObjectName("brand")

        brand_sub = QLabel("SECURITY CONSOLE")
        brand_sub.setObjectName("brandSub")

        brand_text.addWidget(brand)
        brand_text.addWidget(brand_sub)

        brand_row.addWidget(mark)
        brand_row.addLayout(brand_text)
        brand_row.addStretch()

        layout.addLayout(brand_row)
        layout.addSpacing(22)

        self.nav_buttons = []

        sections = [
            (
                "MONITORING",
                [
                    ("▤", "Dashboard", "dashboard"),
                    ("◎", "Risk Analysis", "risk"),
                    ("≡", "Activations", "activations"),
                ],
            ),
            (
                "OPERATIONS",
                [
                    ("⬆", "Model Upload", "upload"),
                    ("▶", "Scan Engine", "scan"),
                    ("⧗", "Scan History", "history"),
                ],
            ),
            (
                "REPORTING",
                [
                    ("⧉", "JSON Reports", "json"),
                    ("⎙", "PDF Reports", "pdf"),
                ],
            ),
        ]

        for section_title, items in sections:
            section = QLabel(section_title)
            section.setObjectName("navSection")
            layout.addWidget(section)
            layout.addSpacing(2)

            for glyph, name, key in items:
                button = QPushButton(f"  {glyph}   {name}")
                button.setObjectName("nav")
                button.setCheckable(True)
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                button.setIconSize(QSize(16, 16))
                button.clicked.connect(
                    lambda _checked, b=button, k=key:
                    self._handle_nav(b, k)
                )
                layout.addWidget(button)
                self.nav_buttons.append(button)

            layout.addSpacing(14)

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

        layout.addStretch()

        engine_state = QFrame()
        engine_state.setStyleSheet(
            f"background-color:{BG_ELEVATED};"
            f"border:1px solid {BORDER}; border-radius:12px;"
        )
        engine_layout = QVBoxLayout(engine_state)
        engine_layout.setContentsMargins(14, 12, 14, 12)
        engine_layout.setSpacing(4)

        engine_title = QLabel("DETECTION ENGINE")
        engine_title.setStyleSheet(
            f"color:{TEXT_MUTED}; font-size:10px;"
            "font-weight:700; letter-spacing:1.2px; border:none;"
        )

        engine_value = QLabel("● Online — Offline Mode")
        engine_value.setStyleSheet(
            f"color:{SUCCESS}; font-size:12px;"
            "font-weight:600; border:none;"
        )

        engine_layout.addWidget(engine_title)
        engine_layout.addWidget(engine_value)

        layout.addWidget(engine_state)

        version = QLabel("v1.0.0  •  Local Analysis Only")
        version.setStyleSheet(
            f"color:{TEXT_MUTED}; font-size:11px; padding-top:10px;"
        )
        layout.addWidget(version)

        sidebar.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        return sidebar

    def _select_nav(self, button):
        """Keep sidebar navigation single-select."""
        for nav_button in self.nav_buttons:
            nav_button.setChecked(nav_button is button)

    # ---- sidebar actions --------------------------------

    def _handle_nav(self, button, key):
        """Run the action bound to a sidebar navigation item."""

        self._select_nav(button)

        if key == "upload":
            self.dashboard.select_model_folder()
            return

        if key == "json":
            self._show_json_reports()
            return

        if key == "pdf":
            self._open_pdf_report()
            return

        titles = {
            "dashboard": "AI SECURITY SCORE",
            "risk": "AI SECURITY SCORE",
            "activations": "ACTIVATION SUMMARY",
            "scan": "SCAN PROGRESS",
            "history": "SCAN HISTORY",
        }

        self._scroll_to_group(titles.get(key))

    def _scroll_to_group(self, title):
        """Scroll the dashboard to the requested section."""

        if not title:
            return

        scroll_area = self.dashboard.findChild(QScrollArea)

        for group in self.dashboard.findChildren(QGroupBox):
            if group.title() != title:
                continue

            if scroll_area is not None:
                scroll_area.ensureWidgetVisible(group, 0, 60)
            else:
                group.setFocus()

            self.statusBar().showMessage(f"Showing {title.title()}", 2500)
            return

        self.statusBar().showMessage(f"{title.title()} not available", 2500)

    # ---- reporting --------------------------------------

    def _report_path(self, name):
        """Resolve a report path relative to the project root."""

        candidates = [
            Path("reports") / name,
            Path(__file__).resolve().parent.parent / "reports" / name,
        ]

        for candidate in candidates:
            if candidate.exists():
                return candidate

        return None

    def _show_json_reports(self):
        """Display the generated JSON reports in a viewer dialog."""

        files = ["scan_summary.json", "layer_statistics.json"]

        found = [(name, self._report_path(name)) for name in files]
        found = [(name, path) for name, path in found if path is not None]

        if not found:
            QMessageBox.warning(
                self,
                "JSON Reports",
                "No JSON reports found.\n\n"
                "Run a scan to generate scan_summary.json and "
                "layer_statistics.json.",
            )
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("NeuroFence — JSON Reports")
        dialog.resize(820, 640)
        dialog.setStyleSheet(APP_STYLESHEET)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        tabs = QTabWidget()

        for name, path in found:
            viewer = QTextEdit()
            viewer.setReadOnly(True)
            viewer.setStyleSheet(
                f"background-color:{BG_ELEVATED}; color:{TEXT};"
                f"border:1px solid {BORDER}; border-radius:10px;"
                "font-family:'JetBrains Mono','Consolas',monospace;"
                "font-size:12px; padding:10px;"
            )

            try:
                with path.open("r", encoding="utf-8") as file:
                    viewer.setPlainText(
                        json.dumps(json.load(file), indent=4)
                    )
            except (OSError, ValueError) as error:
                viewer.setPlainText(f"Unable to read {path}: {error}")

            tabs.addTab(viewer, name)

        layout.addWidget(tabs)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.exec()

    def _open_pdf_report(self):
        """Open the generated PDF report with the system viewer."""

        path = self._report_path("NeuroFence_Report.pdf")

        if path is None:
            QMessageBox.warning(
                self,
                "PDF Report",
                "NeuroFence_Report.pdf was not found.\n\n"
                "Run a scan to generate the report.",
            )
            return

        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            elif os.name == "nt":
                os.startfile(str(path))  # noqa: S606
            else:
                subprocess.Popen(["xdg-open", str(path)])

            self.statusBar().showMessage(f"Opened {path.name}", 3000)
        except OSError as error:
            QMessageBox.critical(
                self,
                "PDF Report",
                f"Unable to open the report:\n{error}",
            )

    # ---- menu -------------------------------------------

    def _create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open_action = QAction("Open Model", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(
            self.dashboard.select_model_folder
        )

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        scan_menu = menu.addMenu("Scan")

        start_action = QAction("Start Scan", self)
        start_action.setShortcut("Ctrl+R")
        start_action.triggered.connect(self.dashboard.start_scan)

        stop_action = QAction("Stop Scan", self)
        stop_action.triggered.connect(self.dashboard.stop_scan)

        scan_menu.addAction(start_action)
        scan_menu.addAction(stop_action)

        help_menu = menu.addMenu("Help")

        about_action = QAction("About NeuroFence", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

    # ---- status bar -------------------------------------

    def _create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        self.state_label = QLabel("● Ready")
        self.state_label.setStyleSheet(
            f"color:{SUCCESS}; font-weight:600;"
        )

        self.mode_label = QLabel("Offline Sandbox")
        self.mode_label.setStyleSheet(f"color:{TEXT_MUTED};")

        self.engine_label = QLabel("Detection Engine: Ready")
        self.engine_label.setStyleSheet(f"color:{TEXT_MUTED};")

        status_bar.addPermanentWidget(self.engine_label)
        status_bar.addPermanentWidget(self._separator())
        status_bar.addPermanentWidget(self.mode_label)
        status_bar.addPermanentWidget(self._separator())
        status_bar.addPermanentWidget(self.state_label)

        status_bar.showMessage("Ready")

    def _separator(self):
        line = QLabel("│")
        line.setStyleSheet(f"color:{BORDER};")
        return line

    def _update_state_label(self, message: str):
        """Mirror dashboard status into the status bar indicator."""
        self.state_label.setText(f"● {message}")
        self.engine_label.setText(f"Detection Engine: {message}")

    # ---- about ------------------------------------------

    def show_about(self):
        QMessageBox.about(
            self,
            "About NeuroFence",
            (
                "NeuroFence\n\n"
                "Offline LLM Weight Poisoning "
                "and Backdoor Scanner"
            ),
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("NeuroFence")
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()