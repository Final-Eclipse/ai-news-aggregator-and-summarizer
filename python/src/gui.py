from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
import requests, json, time, asyncio, aiohttp
from top_bar import TopBar
from main_display import MainDisplay
from pagination import Pagination
from services.localhosts import Localhosts
import asyncio
from settings import Settings
from dotenv import load_dotenv, set_key, find_dotenv
import os
from pathlib import Path

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()

        # Replace all "N/A" fields with empty strings "" for consistency.
        # Some News API results can have empty strings like urlToImage.

        # Use .env file to save api key.
        # When user types api key, replace it in the .env file.
        # When the app runs, read the .env file, if there is an api key, display it as dots in the settings page.
        # When the user hovers over the api key or clicks an eye icon, reveal the api key.
        # https://search.brave.com/search?q=what+is+a+.env+file&conversation=0982ab20246ee8933f695b0cdb71148d6c18
        # https://search.brave.com/search?q=how+to+save+api+key+that+user+types+in+local+host&conversation=0982c3b9c9638409533ee17707b344ba0b52

        # Implement way to get api key.
        # Implement way to get local Ollama models.
        # Implement button to refresh models.
        # Implement way to get summary button.

        # self.run_refresh_models() # Initializes the models available.

        # Implement input fields to allow user to set query parameters and the type of endpoint.
        # Have a reset to defaults button as well under these.

        # Run localhosts.
        threadpool = QThreadPool().globalInstance()
        self.localhosts = Localhosts()
        threadpool.start(self.localhosts)

        # Initialize GUI element objects.
        self.top_bar = TopBar() # Try making the dropdowns QListWidgets or QComboBoxes but when an option is chosen, append the chosen option to any other options there already.
        self.top_bar.settings_button_clicked.connect(self._switch_to_settings)

        self.settings = Settings()
        self.settings.back_button_clicked.connect(self.switch_to_main_gui)

        # Initialize api key label text and create .env file if not exists.
        path = find_dotenv()
        if path == "":
            self._create_env()
        load_dotenv(path)
        api_key = os.getenv("NEWS_API_KEY")
        self.settings.api_key_label.field.setText(api_key)

        self.main_display = MainDisplay()
        self.main_display.show_summary.connect(lambda page: self.switch_to_summary(page))
        self.main_display.remove_summary.connect(self.switch_to_main_gui)

        self.pagination = Pagination()

        # Initialize pagination connections.
        self.pagination.previous_page_button.clicked.connect(self.main_display.previous_page)
        self.pagination.next_page_button.clicked.connect(self.main_display.next_page)
        self.main_display.page_changed.connect(lambda page: self.pagination.current_page_label.setText(str(page)))

        # Fetching results from the database returns a list of tuples of results.
        # Using results directly from News API returns a dictionary of results.
        # If using News API, have to rework news_card.py to init fields using article[key] instead of article[index].
        self.top_bar.endpoint_response.connect(lambda response: self.main_display._set_articles(response))
        self.top_bar.endpoint_response.connect(lambda: self.main_display.update(reset_pages=True))
        # self.top_bar.signals.database_results_stored.connect(lambda: self.main_display._set_articles(self.top_bar.get_database_results()))
        # self.top_bar.signals.database_results_stored.connect(lambda: self.main_display.update(reset_pages=True))

        self.main_gui = self.get_main_gui(self.create_main_gui_layout())
        self.container = QStackedWidget()
        self.container.addWidget(self.main_gui)
        self.container.setCurrentIndex(0)

        self.setCentralWidget(self.container)
        self.setMinimumSize(750, 750)

    def _create_env(self) -> None:
        with open(f"{Path.cwd()}/src/.env", "w+") as file:
            file.write("NEWS_API_KEY=''")

    def _switch_to_settings(self) -> None:
        self.container.setParent(None)
        self.setCentralWidget(self.settings.container)

    def switch_to_summary(self, page: QWidget) -> None:
        self.container.setParent(None)
        self.setCentralWidget(page)

    def switch_to_main_gui(self) -> None:
        self.settings.container.setParent(None)
        self.setCentralWidget(self.container)

    def create_main_gui_layout(self) -> QVBoxLayout:
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

        return layout

    def get_main_gui(self, layout: QVBoxLayout) -> QWidget:
        container = QWidget()
        # container.setStyleSheet("background-color: #c8c8c8")
        container.setLayout(layout)
        return container
    
    def closeEvent(self, a0) -> None:
        self.localhosts.stop()
        return super().closeEvent(a0)
        
def main():  
    app = QApplication([])
    window = Gui()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()