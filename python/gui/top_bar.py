from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker
from everything import Everything
from top_headlines import TopHeadlines
from sources import Sources

class TopBar(QMainWindow):
    def __init__(self):
        super().__init__()

        Everything.init()
        TopHeadlines.init()
        Sources.init()

        self.endpoints = {
            "everything": Everything.parameters,
            "top headlines": TopHeadlines.parameters,
            "sources": Sources.parameters
        }

        self.endpoint_selector: QComboBox = self.__create_endpoint_selector()
        self.endpoint_selector.currentIndexChanged.connect(self.__update_sidebar)

        self.setWindowTitle("")
        self.setCentralWidget(self.__create_layout())

    def get_sidebar_container(self):
        return self.container

    def __update_sidebar(self):   
        match self.endpoint_selector.currentText():
            case "Everything":
                Everything.show()
                TopHeadlines.hide()
                Sources.hide()
                self.placeholder.hide()

            case "Top headlines":
                Everything.hide()
                TopHeadlines.show()
                Sources.hide()
                self.placeholder.hide()

            case "Sources":
                Everything.hide()
                TopHeadlines.hide()
                Sources.show()
                self.placeholder.hide()

            case _:
                Everything.hide()
                TopHeadlines.hide()
                Sources.hide()
                self.placeholder.show()

    def __create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)

        layout.addWidget(self.__create_endpoint_selector_container())

        layout.addWidget(Everything.container)
        layout.addWidget(TopHeadlines.container)
        layout.addWidget(Sources.container)
        layout.addWidget(self.__create_placeholder())

        self.container = QWidget()
        self.container.setLayout(layout)
        self.container.setFixedHeight(130)
        
        return self.container
    
    def __create_placeholder(self) -> QWidget:
        self.placeholder = QWidget()
        return self.placeholder
    
    def __create_endpoint_selector(self):
        endpoint_selector = QComboBox()
        endpoint_selector.setFixedWidth(200)
        endpoint_selector.addItems(["Select an endpoint type", "Everything", "Top headlines", "Sources"])
        return endpoint_selector
    
    def __create_endpoint_selector_container(self):
        layout = QVBoxLayout()

        label = QLabel("Endpoint type")
        label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(label)

        layout.addWidget(self.endpoint_selector)

        container = QWidget()
        container.setLayout(layout)
        
        return container
    
def main():  
    app = QApplication([])
    window = TopBar()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()