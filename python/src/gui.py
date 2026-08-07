from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
import requests, json, time, asyncio, aiohttp
from top_bar import TopBar
from main_display import MainDisplay
from pagination import Pagination

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()

        # Implement way to get api key.
        # Implement way to get local Ollama models.
        # Implement button to refresh models.
        # Implement way to get summary button.

        # self.run_refresh_models() # Initializes the models available.
        # Localhosts.run_localhosts()

        # Implement input fields to allow user to set query parameters and the type of endpoint.
        # Have a reset to defaults button as well under these.

        self.top_bar = TopBar()
        self.main_display = MainDisplay()
        self.pagination = Pagination()

        self.pagination.previous_page_button.clicked.connect(self.main_display.previous_page)
        self.pagination.previous_page_button.clicked.connect(lambda: self.pagination.current_page_label.setText(str(self.main_display.current_page_number)))

        self.pagination.next_page_button.clicked.connect(self.main_display.next_page)
        self.pagination.next_page_button.clicked.connect(lambda: self.pagination.current_page_label.setText(str(self.main_display.current_page_number)))
        
        self.top_bar.signals.database_results_stored.connect(lambda: self.main_display.update(self.top_bar.get_database_results()))
        
        self.container: QWidget = self.create_layout()
        self.setCentralWidget(self.container)
        self.setMinimumSize(750, 750)

    def create_layout(self) -> QWidget:
        layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add top bar
        top_bar_container: QWidget = self.top_bar.get_container()
        layout.addWidget(top_bar_container)

        # Add main display
        main_display_container: QWidget = self.main_display.container
        layout.addWidget(main_display_container)

        # Add pagination bar
        pagination_container: QWidget = self.pagination.container
        layout.addWidget(pagination_container)

        container = QWidget()
        # container.setStyleSheet("background-color: #c8c8c8")
        container.setLayout(layout)
        return container
        
def main():  
    app = QApplication([])
    window = Gui()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()