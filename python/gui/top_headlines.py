from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker

class TopHeadlines():
    parameters = {}
    container: QWidget = None

    @staticmethod
    def init() -> None:
        TopHeadlines.init_parameters()
        layout = TopHeadlines.__create_layout()
        TopHeadlines.__create_container(layout)
        TopHeadlines.__init_fields()
        TopHeadlines.hide()

    @staticmethod
    def init_parameters() -> None:
        TopHeadlines.parameters = {
            "country": QComboBox(),
            "category": QComboBox(),
            "sources": QComboBox(),
            "query": QLineEdit(),
            "pageSize": QLineEdit(),
            "page": QLineEdit()
        }

    @staticmethod
    def __init_fields() -> None:
        parameters = TopHeadlines.parameters

        country: QComboBox = parameters["country"]
        country.addItems(["Select country", "United States", "Canada", "Mexico"])

        category: QComboBox = parameters["category"]
        category.addItems(["Select category", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])

        sources: QComboBox = parameters["sources"]
        sources.addItems(["Select source(s)", "ABC News", "Associated Press"])

        query: QLineEdit = parameters["query"]
        query.setPlaceholderText("Type query")

        pageSize: QLineEdit = parameters["pageSize"]
        pageSize.setPlaceholderText("Type page size")

        page: QLineEdit = parameters["page"]
        page.setPlaceholderText("Type page number")

    @staticmethod
    def __create_layout() -> QGridLayout:
        layout = QGridLayout()

        row = 0
        col = 0
        for key, widget in TopHeadlines.parameters.items():
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
        TopHeadlines.container = container
    
    @staticmethod
    def hide() -> None:
        container: QWidget = TopHeadlines.container
        container.hide()

    @staticmethod
    def show() -> None:
        container: QWidget = TopHeadlines.container
        container.show()