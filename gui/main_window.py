import os
import sys

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)

from dashboard import Dashboard


class MainWindow(QMainWindow):
    """Main window for the NeuroFence application."""

    def __init__(self):
        super().__init__()
        self.dashboard = Dashboard()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("NeuroFence")
        self.setFixedSize(1000, 700)

        icon_path = os.path.join("assets", "icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setCentralWidget(self.dashboard)

        self._create_menu()

        self.statusBar().showMessage("Ready")

        self.dashboard.status_changed.connect(
            self.statusBar().showMessage
        )

    def _create_menu(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("File")

        open_action = QAction("Open Model", self)
        open_action.triggered.connect(
            self.dashboard.select_model_folder
        )

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        help_menu = menu.addMenu("Help")

        about_action = QAction("About NeuroFence", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

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

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()