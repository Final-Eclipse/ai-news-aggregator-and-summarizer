from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
import requests
from random import randint

# Rename file and class from MainDisplay to NewsCard?
class Pagination(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.previous_page_button = QPushButton("Previous page")
        self.next_page_button = QPushButton("Next page")

        self.current_page_number = 1
        self.current_page_label = QLabel(f"{self.current_page_number}")
        self.current_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.container: QWidget = self._create_container()

        self.setCentralWidget(self.container)

    def _create_container(self) -> QWidget:
        container = QWidget()
        layout = self._create_layout()
        container.setLayout(layout)
        return container

    def _create_layout(self) -> None:
        layout = QHBoxLayout()
        layout.addWidget(self.previous_page_button)
        layout.addWidget(self.current_page_label)
        layout.addWidget(self.next_page_button)
        return layout

def main() -> None:  
    app = QApplication([])
    window = Pagination()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()