import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from dashboard import Dashboard


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("NeuroFence")
        self.setFixedSize(1000, 700)

        self.setCentralWidget(Dashboard())

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About")

        self.statusBar().showMessage("Ready")


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()