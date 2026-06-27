from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, pyqtSignal, QRunnable
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker
from top_bar import TopBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.run_refresh_models() # Initializes the models available.
        # Localhosts.run_localhosts()

        # Implement input fields to allow user to set query parameters and the type of endpoint.
        # Have a reset to defaults button as well under these.

        self.top_bar = TopBar()

        self.summarize_button = QPushButton("Summarize article")
        self.summary_text = QLabel("I haven't implemented the summary yet.")

        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Enter News API key")

        self.available_models = QComboBox()
        self.button = QPushButton("Clear local Ollama models")
        self.button.clicked.connect(lambda: self.available_models.clear())

        self.refresh_button = QPushButton("Refresh local Ollama models")
        self.models_text_box = QLabel()
        self.refresh_button.clicked.connect(self.run_refresh_models)
        
        self.setWindowTitle("My App")
        
        self.result = QLabel()
        self.result.setWordWrap(True)
        self.result.setFixedSize(QSize(self.width(), self.height()))
    
        self.send_button = QPushButton("Send endpoint data")
        self.send_button.clicked.connect(self.send_endpoint_data)

        self.get_button = QPushButton("Get endpoint data")
        self.get_button.clicked.connect(self.get_endpoint_json)
        
        self.setCentralWidget(self.create_layout())

    def populate_available_models(self, models: OllamaModelsDto):
        self.available_models.clear()
        self.available_models.addItems(models.local_models["localModels"])

    def run_refresh_models(self):
        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.get_models)

        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker.local_models.connect(lambda models: self.models_text_box.setText(str(models.local_models)))
        self.worker.local_models.connect(self.populate_available_models)

        self.worker_thread.start()

    def update_models_text_box(self, text):
        self.models_text_box.setText(text)

    def create_layout(self):
        layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)

        # Add top bar
        layout.addWidget(self.top_bar.get_top_bar_container())

        layout.addWidget(self.get_post_endpoint_data())
        layout.addWidget(self.send_button)
        layout.addWidget(self.get_endpoint_types())
        layout.addWidget(self.get_button)
        layout.addWidget(self.result)
        layout.addWidget(self.available_models)
        layout.addWidget(self.button)
        layout.addWidget(self.api_key)

        layout.addWidget(self.refresh_button)
        layout.addWidget(self.models_text_box)
        
        layout.addWidget(self.summarize_button)
        layout.addWidget(self.summary_text)

        container = QWidget()
        container.setStyleSheet("background-color: #c8c8c8")
        container.setLayout(layout)
        return container
    
    @staticmethod
    def create_everything():
        """Returns a JSON string."""
        query_params = {
            "endpoint": "everything",
            "q": "trump",
            "searchIn": None,
            "sources": "associated-press",
            "domains": None,
            "excludeDomains": None,
            "from": MainWindow.get_oldest_date(),
            "to": MainWindow.get_current_date(),
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": "100",
            "page": "1" 
        }

        return json.dumps(query_params)

    def send_endpoint_data(self):
        headers = {"Content-Type": "application/json"}
        requests.post("http://localhost:8080/api/v1/news/post-endpoint-data", data=MainWindow.create_everything(), headers=headers)
    
    def update_result(self, text):
        self.result.setText(text)

    def get_endpoint_json(self):
        request = requests.get(f"http://localhost:8080{self.endpoint_types.currentText()}")
        response = request.text
        self.update_result(response)

    def get_post_endpoint_data(self):
        post_endpoint_data = QLabel("/api/v1/news/post-endpoint-data")
        return post_endpoint_data
    
    def get_endpoint_types(self):
        self.endpoint_types = QComboBox()
        self.endpoint_types.addItems(["/api/v1/news/everything", "/api/v1/news/top-headlines", "/api/v1/news/top-headlines/sources"])
        return self.endpoint_types
    
    @staticmethod
    def get_current_date():
        """Returns the current date."""
        local_time = time.localtime()
        year = time.strftime("%Y", local_time)
        month = time.strftime("%m", local_time)
        day = time.strftime("%d", local_time)
        date = f"{year}-{month}-{day}"

        return date

    @staticmethod
    def get_oldest_date():
        "Returns a date for the furthest back the NewsAPI allows (one month back) in ISO 8601 format."
        current_date = MainWindow.get_current_date()
        month = int(current_date[5:7]) - 1
        year = int(current_date[0:4])
        day = int(current_date[8:]) + 1

        # Changes month to December and year to previous if needed.
        if month <= 0:
            month = 12
            year -= 1
        

        # Prefixes a 0 to the month and day if needed.
        if month < 10:
            month = f"0{month}"
        if day < 10:
            day = f"0{day}"

        oldest_date = f"{year}-{month}-{day}"
        return oldest_date
        
def main():  
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
    # asyncio.run(main())