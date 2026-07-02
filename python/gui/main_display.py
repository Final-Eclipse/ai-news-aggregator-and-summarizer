from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
import requests, json, time, asyncio, aiohttp
from localhosts import Localhosts
from ollama_models import OllamaModels
from ollama_models_dto import OllamaModelsDto
from http_service import HttpService    
from worker import Worker
from everything import Everything
from top_headlines import TopHeadlines
from sources import Sources
from random import randint

# Rename file and class from MainDisplay to NewsCard?
class MainDisplay(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Main Display")

        # self.setCentralWidget(self.create_container())
        self.setCentralWidget(self.create_news_container())

    def get_container(self):
        return self.create_news_container()
    #     return self.create_container()
    
    def create_desc_container(self):
        container = QWidget()
        # container.setStyleSheet("background-color: red")
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        news_outlet = QLabel("Associated Press")
        news_outlet.setMaximumSize(news_outlet.sizeHint().width(), news_outlet.sizeHint().height())
        # news_outlet.setStyleSheet(f"background-color: rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})")
        layout.addWidget(news_outlet, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)

        brief_desc = QLabel("A Trump order asked national park visitors to flag 'negative' historical info. They had other ideas")
        brief_desc.setMaximumSize(brief_desc.sizeHint().width(), brief_desc.sizeHint().height())
        # brief_desc.setStyleSheet(f"background-color: rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})")
        layout.addWidget(brief_desc, 1, 0)

        author = QLabel("AP")
        author.setMaximumSize(author.sizeHint().width(), author.sizeHint().height())
        # author.setStyleSheet(f"background-color: rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})")
        layout.addWidget(author, 2, 0, alignment=Qt.AlignmentFlag.AlignRight)

        container.setLayout(layout)

        offset = 1.2
        width = int(layout.sizeHint().width() * offset)
        height = int(layout.sizeHint().height() * offset)
        container.setMaximumSize(width, height)
        
        return container
    
    def create_news_container(self):
        container = QWidget()
        # container.setStyleSheet("background-color: blue")

        layout = QHBoxLayout()

        thumbnail = self.create_thumbnail()
        layout.addWidget(thumbnail)

        desc_container = self.create_desc_container()
        layout.addWidget(desc_container, alignment=Qt.AlignmentFlag.AlignLeft)

        width = int(thumbnail.width() + desc_container.width())
        height = int(thumbnail.height() + desc_container.height())
        
        container.setLayout(layout)
        container.setMaximumSize(width, height)

        return container

    # def create_layout(self) -> QGridLayout:
    #     layout = QGridLayout()

    #     # Add thumbnails
    #     thumbnails = self.create_thumbnails()
    #     for thumbnail, row_col in thumbnails.items():
    #         layout.addWidget(thumbnail, row_col[0], row_col[1])
        
    #     return layout

    # def create_container(self) -> QWidget:
    #     layout = self.create_layout()
    #     # layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    #     container = QWidget()
    #     container.setLayout(layout)

    #     return container
    
    def create_thumbnail(self) -> QLabel:
        pixmap_data = requests.get(f"https://bloximages.chicago2.vip.townnews.com/thesunchronicle.com/content/tncms/assets/v3/editorial/8/63/8633a847-b25a-5cac-9261-cd9a433fb5e2/6a298f4a043f2.image.jpg?crop=1763%2C926%2C0%2C124&resize=1200%2C630&order=crop%2Cresize").content
        # pixmap_data = requests.get(f"https://dims.apnews.com/dims4/default/35479c0/2147483647/strip/true/crop/7600x5064+0+1/resize/980x653!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2F7c%2Fee%2F4bc97788cc5df7272e46e010bafd%2Fd8d320f7eb794693bdfa131323a9b476").content
        # pixmap_data = requests.get(f"https://dims.apnews.com/dims4/default/7af89c8/2147483647/strip/true/crop/5048x3364+0+1/resize/980x653!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Ff4%2Ff3%2F659d9e3f601ca643b5c07b9142e0%2F51bbebdb10f74e82bea3dbf556b64607").content

        thumbnail = QLabel()
        thumbnail.setScaledContents(True)

        pixmap = QPixmap()
        pixmap.loadFromData(pixmap_data)
        
        thumbnail.setMaximumSize(150, 150)
        thumbnail.setPixmap(pixmap)
        # thumbnail.setStyleSheet(f"background-color: rgba({randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)}, {randint(0, 255)})")

        return thumbnail

def main() -> None:  
    app = QApplication([])
    window = MainDisplay()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()