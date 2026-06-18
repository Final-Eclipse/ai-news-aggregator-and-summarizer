from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QSize
import requests, json, time
from localhosts import Localhosts
from ollama_models import OllamaModels

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Localhosts.run_localhosts()
        # self.ollama_models = OllamaModels.fetch_ollama_models()
        
        self.setWindowTitle("My App")
        
        self.result = QLabel()
        self.result.setWordWrap(True)
        self.result.setFixedSize(QSize(self.width(), self.height()))
    
        self.send_button = QPushButton("Send endpoint data")
        self.send_button.clicked.connect(self.send_endpoint_data)

        self.get_button = QPushButton("Get endpoint data")
        self.get_button.clicked.connect(self.get_endpoint_json)
        
        self.setCentralWidget(self.create_layout())

    def create_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.get_post_endpoint_data())
        layout.addWidget(self.send_button)
        layout.addWidget(self.get_endpoint_types())
        layout.addWidget(self.get_button)
        layout.addWidget(self.result)

        container = QWidget()
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


        
        
app = QApplication([])
window = MainWindow()
window.show()
app.exec()