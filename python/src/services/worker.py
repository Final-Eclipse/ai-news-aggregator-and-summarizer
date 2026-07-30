from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot
import requests
from database import database

class EndpointDataWorker(QRunnable):
    def __init__(self) -> None:
        super().__init__()
        self.signal = Signals() # Emits signal when finished.

    @pyqtSlot()
    def run(self) -> None:
        """Send POST request to upload endpoint data."""
        headers = {"Content-Type": "application/json"}
        request = requests.post(f"http://localhost:8080/api/v1/news/post-endpoint-data", data=self.query_parameters, headers=headers)
        self.signal.upload_finished.emit()

    def set_query_parameters(self, query_parameters: str) -> None:
        """
        Set query parameters to be sent in the body of the POST request.

        @param query_parameters: JSON formatted string of query parameters to send in the body of the POST request.
        """
        self.query_parameters = query_parameters

class EndpointResponseWorker(QRunnable):  
    def __init__(self, endpoint_type: str) -> None:
        """
        Initialize instance.
        
        @param endpoint_type: String value of the current endpoint type.
        """
        super().__init__()
        self.signal = Signals() # Emits signal when finished.
        self.endpoint_type = endpoint_type

    @pyqtSlot()
    def run(self) -> None:
        """Send GET request to retrieve and emit signal containing News API result."""
        request = requests.get(f"http://localhost:8080/api/v1/news/{self.endpoint_type}")  # Change endpoint depending on endpoint data.
        response = request.json()

        self.signal.response_finished.emit(response)

class DatabaseWorker(QRunnable):
    def __init__(self, endpoint_type: str, response: dict) -> None:
        """
        Initialize instance.

        @param endpoint_type: String value of the current endpoint type.
        @param response: Dictionary object converted from JSON receieved from News API.
        """
        super().__init__()
        self.endpoint_type = endpoint_type
        self.response = response

    @pyqtSlot()
    def run(self) -> None:
        """Create database table if necessary and add data to it depending on the endpoint type."""
        match self.endpoint_type:
            case "everything":
                database.create_table_everything()  # Creates table if it does not exist already.
                database.add_to_table_everything(self.response)

            case "top-headlines":
                database.create_table_top_headlines()
                database.add_to_table_top_headlines(self.response)

            case "top-headlines/sources":
                database.create_table_sources()
                database.add_to_table_sources(self.response)

            case _:
                raise Exception("[run() in worker.py] Endpoint type does not match any valid ones.")

class DatabaseQueryWorker(QRunnable):
    def __init__(self, endpoint_type: str, bindings: dict) -> None:
        """
        Initialize instance.

        @param endpoint_type: String value of the current endpoint type.
        @param response: Dictionary object converted from JSON receieved from News API.
        """
        super().__init__()
        self.endpoint_type = endpoint_type
        self.bindings = bindings
        self.signal = Signals()

    @pyqtSlot()
    def run(self) -> None:
        match self.endpoint_type:
            case "everything":
                result = database.query_table_everything(self.bindings)
                self.signal.query_finished.emit(result)
            case _:
                raise Exception("[run() in worker.py] Endpoint type does not match any valid ones.")

class Signals(QObject):
    # EndpointDataWorker
    upload_finished = pyqtSignal()
    
    # EndpointResponseWorker
    response_finished = pyqtSignal(dict)

    # DatabaseQueryWorker
    query_finished = pyqtSignal(list)