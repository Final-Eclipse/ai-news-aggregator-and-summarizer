from PyQt5.QtCore import QObject, pyqtSignal, QThread, QRunnable, pyqtSlot
from services.http_service import HttpService
import requests


# class Worker(QObject):
#     # Global
#     finished = pyqtSignal()

#     # Local models
#     local_models = pyqtSignal(dict)

#     # Send post request
#     post_request_finished = pyqtSignal(str)

#     # Get json response
#     json_response_finished = pyqtSignal(dict)

#     def get_models(self) -> str:
#         result = HttpService.get_local_ollama_models()
   
#         self.local_models.emit(result)
#         self.finished.emit()

#     def post_endpoint_data(self, query_parameters) -> str:
#         headers = {"Content-Type": "application/json"}
#         request = requests.post(f"http://localhost:8080/api/v1/news/post-endpoint-data", data=query_parameters, headers=headers)
        
#         self.finished.emit()
#         self.post_request_finished.emit(request.text)
    
#     def get_json_response(self) -> dict:
#         request = requests.get("http://localhost:8080/api/v1/news/everything").json()
#         self.json_response_finished.emit(request)

class EndpointDataWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signal = Signals()

    @pyqtSlot()
    def run(self):
        headers = {"Content-Type": "application/json"}
        request = requests.post(f"http://localhost:8080/api/v1/news/post-endpoint-data", data=self.query_parameters, headers=headers)
        self.signal.upload_finished.emit()

    def set_query_parameters(self, query_parameters):
        self.query_parameters = query_parameters

class EndpointResponseWorker(QRunnable):  
    def __init__(self):
        super().__init__()
        self.signal = Signals()

    @pyqtSlot()
    def run(self):
        request = requests.get("http://localhost:8080/api/v1/news/everything")  # Change endpoint depending on endpoint data.
        response = request.json()

        self.signal.response_finished.emit(response)

class Signals(QObject):
    # EndpointDataWorker
    upload_finished = pyqtSignal()
    
    # EndpointResponseWorker
    response_finished = pyqtSignal(dict)