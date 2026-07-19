from PyQt5.QtCore import QObject, pyqtSignal
from services.http_service import HttpService
import requests


class Worker(QObject):
    # Global
    finished = pyqtSignal()

    # Local models
    local_models = pyqtSignal(dict)

    # Send post request
    post_request_finished = pyqtSignal(str)

    def get_models(self) -> str:
        result = HttpService.get_local_ollama_models()
   
        self.local_models.emit(result)
        self.finished.emit()

    def send_post_request(self, query_parameters) -> str:
        headers = {"Content-Type": "application/json"}
        request = requests.post(f"http://localhost:8080/api/v1/news/post-endpoint-data", data=query_parameters, headers=headers)
        
        self.finished.emit()
        self.post_request_finished.emit(request.text)
        