from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QGridLayout
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker

class Everything():
    parameters = {}
    container: QWidget = None

    @staticmethod
    def init() -> None:
        Everything.init_parameters()
        layout = Everything.__create_layout()
        Everything.__create_container(layout)
        Everything.__init_fields() 
        Everything.hide()

    @staticmethod
    def init_parameters() -> None:
        Everything.parameters = {
            "query": QLineEdit(),
            "searchIn": QComboBox(),  
            "sources": QComboBox(),
            "domains": QComboBox(),
            "excludeDomains": QComboBox(),
            "from": QLineEdit(),
            "to": QLineEdit(),
            "language": QComboBox(),
            "sortBy": QComboBox(),
            "pageSize": QLineEdit(),
            "page": QLineEdit()
        }

    @staticmethod
    def __init_fields() -> None:
        parameters = Everything.parameters

        query: QLineEdit = parameters["query"]
        query.setPlaceholderText("Type query")

        searchIn: QComboBox = parameters["searchIn"]
        searchIn.addItems(["Select search type(s)", "Title", "Description", "Content"])

        sources: QComboBox = parameters["sources"]
        sources.addItems(["Select source(s)", "ABC News", "Associated Press"])

        domains: QComboBox = parameters["domains"]
        domains.addItems(["Select domain(s)", "BBC", "TechCrunch", "Engadget"])

        excludeDomains: QComboBox = parameters["excludeDomains"]
        excludeDomains.addItems(["Select domain(s) to exclude", "Fox News"])

        from_: QLineEdit = parameters["from"]
        from_.setPlaceholderText("Type start date")

        to: QLineEdit = parameters["to"]
        to.setPlaceholderText("Type end date")

        language: QComboBox = parameters["language"]
        language.addItems(["Select language", "English", "Spanish", "German"])

        sortBy: QComboBox = parameters["sortBy"]
        sortBy.addItems(["Select sort option", "Relevancy", "Popularity", "Date published"])

        pageSize: QLineEdit = parameters["pageSize"]
        pageSize.setPlaceholderText("Type page size")

        page: QLineEdit = parameters["page"]
        page.setPlaceholderText("Type page number")

    @staticmethod
    def __create_layout() -> QGridLayout: 
        layout = QGridLayout()
        
        row = 0
        col = 0
        for key, widget in Everything.parameters.items():
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
        Everything.container = container

    @staticmethod
    def hide() -> None:
        container: QWidget = Everything.container
        container.hide()

    @staticmethod
    def show() -> None:
        container: QWidget = Everything.container
        container.show()