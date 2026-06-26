from PyQt5.QtWidgets import QApplication, QComboBox, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QGridLayout
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker

class Everything():
    def __init__(self) -> None:
        self.parameters: dict = self._init_parameters()

        self.layout: QGridLayout = self._create_layout()
        self.container: QWidget = self._create_container(self.layout)

        self._init_fields()
        self._init_widget_sizes()

        self.hide()

    def _init_parameters(self) -> dict:
        parameters = {
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

        return parameters            

    def _create_layout(self) -> QGridLayout: 
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setHorizontalSpacing(10)
        
        row = 0
        col = 0
        for key, widget in self.parameters.items():
            label = QLabel(key)
            label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            
            layout.addWidget(label, row, col)
            layout.addWidget(widget, row + 1, col)

            col += 1

        return layout
    
    def _create_container(self, layout) -> QWidget:
        container = QWidget()
        container.setLayout(layout)
        return container
    
    def _init_fields(self) -> None:
        parameters = self.parameters

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

    def _init_widget_sizes(self) -> None:
        for key, widget in self.parameters.items():
            widget: QWidget
            max_width = widget.sizeHint().width()
            widget.setMaximumWidth(max_width)

    def hide(self) -> None:
        self.container.hide()

    def show(self) -> None:
        self.container.show()