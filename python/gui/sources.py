from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker

class Sources():
    parameters = {}
    container: QWidget = None

    @staticmethod
    def init() -> None:
        Sources.init_parameters()
        layout = Sources.__create_layout()
        Sources.__create_container(layout)
        Sources.__init_fields()
        Sources.hide()

    @staticmethod
    def init_parameters() -> None:
        Sources.parameters = {
            "category": QComboBox(),
            "language": QComboBox(),
            "country": QComboBox()
        }

    @staticmethod
    def __init_fields() -> None:
        parameters = Sources.parameters
    
        category: QComboBox = parameters["category"]
        category.addItems(["Select category", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])
        
        language: QComboBox = parameters["language"]
        language.addItems(["Select language", "English", "Spanish", "German"])

        country: QComboBox = parameters["country"]
        country.addItems(["Select country", "United States", "Canada", "Mexico"])

    @staticmethod
    def __create_layout() -> QGridLayout:
        layout = QGridLayout()
        
        row = 0
        col = 0
        for key, widget in Sources.parameters.items():
            label = QLabel(key)
            label.setAlignment(Qt.AlignmentFlag.AlignBottom)

            layout.addWidget(label, row, col)
            layout.addWidget(widget, row + 1, col)

            col += 1
        
        return layout
    
    @staticmethod
    def __create_container(layout):
        container: QWidget = QWidget()
        container.setLayout(layout)
        Sources.container = container

    @staticmethod
    def hide() -> None:
        container: QWidget = Sources.container
        container.hide()

    @staticmethod
    def show() -> None:
        container: QWidget = Sources.container
        container.show()