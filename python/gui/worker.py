from PyQt5.QtCore import QObject, pyqtSignal
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService


class Worker(QObject):
    finished = pyqtSignal()
    local_models = pyqtSignal(OllamaModelsDto)

    def get_models(self):
        result = HttpService.get_local_ollama_models()
   
        self.local_models.emit(result)
        self.finished.emit()