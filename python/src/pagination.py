from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
import requests
from random import randint

class Pagination(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.previous_page_button = QPushButton("Previous page")
        # self.previous_page_button.setGeometry(200, 150, 100, 100)
        self.previous_page_button.setFixedSize(self.previous_page_button.sizeHint().width(), 30)
        self.previous_page_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px; border: 2px solid black
            }
            QPushButton:hover {
                background-color: blue
            }
            QPushButton:pressed {
                background-color: red
            }
        """)
        self.next_page_button = QPushButton("Next page")
        self.next_page_button.setFixedSize(self.next_page_button.sizeHint().width(), 30)
        self.next_page_button.setStyleSheet("""
            QPushButton {
                border-radius: 5px; border: 2px solid black
            }
            QPushButton:hover {
                background-color: blue
            }
            QPushButton:pressed {
                background-color: red
            }
        """)

        self.current_page_number = 1
        self.current_page_label = QLabel(f"{self.current_page_number}")
        self.current_page_label.setFixedSize(60, 30)
        self.current_page_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_page_label.setStyleSheet("""
            border-radius: 5px; border: 2px solid black
        """)

        self.container: QWidget = self._create_container()

        self.setCentralWidget(self.container)

    def _create_container(self) -> QWidget:
        container = QWidget()
        # container.setStyleSheet("background-color: #909090")
        # container.setContentsMargins(0, 0, 0, 0)
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