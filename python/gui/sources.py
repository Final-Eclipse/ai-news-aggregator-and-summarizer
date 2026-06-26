from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker

class Sources():
    def __init__(self) -> None:
        self.parameters: dict = self.init_parameters()

        layout: QGridLayout = self._create_layout()
        self.container: QWidget = self._create_container(layout)

        self._init_fields()
        self.hide()
    
    def init_parameters(self) -> dict:
        parameters = {
            "category": QComboBox(),
            "language": QComboBox(),
            "country": QComboBox()
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
    
        category: QComboBox = parameters["category"]
        category.addItems(["Select category", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])
        
        language: QComboBox = parameters["language"]
        language.addItems(["Select language", "English", "Spanish", "German"])

        country: QComboBox = parameters["country"]
        country.addItems(["Select country", "United States", "Canada", "Mexico"])
    
    def _init_widget_sizes(self) -> None:
        for key, widget in self.parameters.items():
            widget: QWidget
            max_width = widget.sizeHint().width()
            widget.setMaximumWidth(max_width)
    
    def hide(self) -> None:
        self.container.hide()
    
    def show(self) -> None:
        self.container.show()