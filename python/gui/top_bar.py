from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont
import requests, json, time, asyncio, aiohttp
from request_api.localhosts import Localhosts
from request_api.ollama_models import OllamaModels
from models.ollama_models_dto import OllamaModelsDto
from request_api.http_service import HttpService    
from request_api.worker import Worker
from news_api_endpoints.everything import Everything
from news_api_endpoints.top_headlines import TopHeadlines
from news_api_endpoints.sources import Sources
from random import randint

class TopBar(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.everything = Everything()
        self.top_headlines = TopHeadlines()
        self.sources = Sources()

        # self.endpoints = {
        #     "everything": self.everything.parameters,
        #     "top headlines": self.top_headlines.parameters,
        #     "sources": self.sources.parameters
        # }

        self.endpoint_selector: QComboBox = self._create_endpoint_selector()
        self.endpoint_selector.currentIndexChanged.connect(self._update_top_bar)

        self.container: QWidget = self._create_layout()

        self.setWindowTitle("")
        self.setCentralWidget(self.container)

    def _receive_endpoint_url(self, url):
        url = url
        print("hello " + url)
        
    def _send_post_request(self) -> str:
        endpoint_type, json_str = self._get_endpoint_data()

        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        
        self.worker_thread.started.connect(lambda: self.worker.send_post_request(json_str))

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        
        self.worker.post_request_finished.connect(self._receive_endpoint_url)
        self.worker_thread.start()
    
    def _get_endpoint_data(self) -> str:
        endpoint_type = self.endpoint_selector.currentText().lower().replace(" ", "-")

        match endpoint_type:
            case "everything":
                json_str = self.everything.get_json(endpoint_type)
            case "top-headlines":
                json_str = self.top_headlines.get_json(endpoint_type)
            case "sources":
                endpoint_type = "top-headlines/sources"
                json_str = self.sources.get_json(endpoint_type)
            case _:
                raise Exception("[_get_endpoint_data in top_bar.py] Endpoint type not selected.")

        # json_str = self.everything.get_json(endpoint_type)   # Ensure to have name as json_str or query_parameters and enforce everywhere for consistency.
        return endpoint_type, json_str

    def get_container(self) -> QWidget:
        return self.container

    def _update_top_bar(self) -> None:   
        match self.endpoint_selector.currentText():
            case "Everything":
                self.everything.show()
                self.top_headlines.hide()
                self.sources.hide()
                self.placeholder.hide()

            case "Top headlines":
                self.everything.hide()
                self.top_headlines.show()
                self.sources.hide()
                self.placeholder.hide()

            case "Sources":
                self.everything.hide()
                self.top_headlines.hide()
                self.sources.show()
                self.placeholder.hide()

            case _:
                self.everything.hide()
                self.top_headlines.hide()
                self.sources.hide()
                self.placeholder.show()

    def _create_layout(self) -> QWidget:
        layout = QVBoxLayout()
        layout.setSpacing(0)

        layout.addWidget(self._create_endpoint_selector_container())
        
        layout.addWidget(self.everything.container)
        layout.addWidget(self.top_headlines.container)
        layout.addWidget(self.sources.container)
        layout.addWidget(self._create_placeholder())

        # Move create container into separate method.
        self.container = QWidget()  # Make into an instance variable.
        # self.container.setStyleSheet(f"background-color: #eeeeee")
        # self.container.setStyleSheet(f"background-color: #D0D0D0")
        self.container.setLayout(layout)
        # fixed_height = int(self.screen().size().height() * 0.12)
        fixed_height = int(self.container.sizeHint().height() * 1.65)   # Works differently on different devices. 
        self.container.setFixedHeight(fixed_height)
        
        return self.container
    
    def _create_placeholder(self) -> QWidget:
        """Blocks the second row in the container when the default dropdown option is selected."""
        self.placeholder = QWidget()
        return self.placeholder
    
    def _create_endpoint_selector(self) -> QComboBox:
        endpoint_selector = QComboBox()        
        endpoint_selector.addItems(["Select an endpoint type", "Everything", "Top headlines", "Sources"])

        max_width = endpoint_selector.sizeHint().width()
        endpoint_selector.setMaximumWidth(max_width)

        return endpoint_selector

    def _create_search_button(self) -> QPushButton:
        search_button = QPushButton("Search")
        search_button.clicked.connect(self._send_post_request)
        # search_button.clicked.connect(self.get_endpoint_data)

        max_width = search_button.sizeHint().width()
        search_button.setMaximumWidth(max_width)
        return search_button
    
    def _create_endpoint_selector_container(self) -> QWidget:
        # layout = QVBoxLayout()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        label = QLabel("Endpoint type")
        label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(label, 0, 0)

        layout.addWidget(self.endpoint_selector, 1, 0)
        layout.addWidget(self._create_search_button(), 1, 1)

        container = QWidget()
        container.setLayout(layout)
        
        return container
    
def main() -> None:  
    app = QApplication([])
    window = TopBar()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()