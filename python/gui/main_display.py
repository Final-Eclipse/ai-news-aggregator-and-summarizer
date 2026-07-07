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
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle("Main Display")

        self.setCentralWidget(self.create_news_container())

    def get_container(self) -> QWidget:
        return self.create_news_container()
    
    def _create_label(self, text: str) -> QLabel:
        label = QLabel(text)
        
        # font = label.font()
        # font.setPointSize(16)
        # label.setFont(font)

        # print(label.width(), label.height())
        # label.setMaximumSize(label.sizeHint().width(), label.sizeHint().height())
        # print(label.sizeHint().width(), label.sizeHint().height())
        # print()
        return label
    
    def _create_desc_container(self) -> QWidget:
        container = QWidget()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        row = 0
        col = 0
        news_outlet = self._create_label("Associated Press")
        layout.addWidget(news_outlet, row, col, alignment=Qt.AlignmentFlag.AlignLeft)

        row += 1
        brief_desc = self._create_label("A Trump order asked national park visitors to flag 'negative' historical info. They had other ideas")
        # Add "..." for long text.
        # brief_desc = self._create_label("afijpoaeijpofwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww john apple today tomorrow cookie ipad food hi")
        layout.addWidget(brief_desc, row, col)

        row += 1
        author = self._create_label("AP")
        layout.addWidget(author, row, col, alignment=Qt.AlignmentFlag.AlignRight)

        container.setLayout(layout)
        # container.setStyleSheet("background-color: blue")

        offset = 1.2
        width = int(layout.sizeHint().width() * offset)
        height = int(layout.sizeHint().height() * offset)

        # container.setMaximumSize(2000, 2000)
        # container.setMaximumSize(width, height)
        container.setMaximumSize(container.sizeHint().width(), container.sizeHint().height())
        
        return container
    
    def create_news_container(self) -> QWidget:
        container = QWidget()
        # container.setStyleSheet("background-color: red")
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        num_of_cards = 4

        for x in range(0, num_of_cards):
            layout.addWidget(self._create_news_card())

        container.setLayout(layout)
        return container

    def _create_news_card(self) -> QWidget:
        container = QWidget()

        layout = QHBoxLayout()
        
        thumbnail = self._create_thumbnail()
        layout.addWidget(thumbnail)

        desc_container = self._create_desc_container()
        layout.addWidget(desc_container, alignment=Qt.AlignmentFlag.AlignLeft)

        width = int(thumbnail.width() + desc_container.width())
        height = int(thumbnail.height() + desc_container.height())
        
        container.setLayout(layout)
        # container.setMaximumSize(width, height)
        container.setMaximumSize(container.sizeHint().width(), container.sizeHint().height())
        # container.setStyleSheet("background-color: pink")

        return container
    
    def _create_thumbnail(self) -> QLabel:
        pixmap_data = requests.get(f"https://bloximages.chicago2.vip.townnews.com/thesunchronicle.com/content/tncms/assets/v3/editorial/8/63/8633a847-b25a-5cac-9261-cd9a433fb5e2/6a298f4a043f2.image.jpg?crop=1763%2C926%2C0%2C124&resize=1200%2C630&order=crop%2Cresize").content

        thumbnail = QLabel()
        thumbnail.setScaledContents(True)

        pixmap = QPixmap()
        pixmap.loadFromData(pixmap_data)
        
        thumbnail.setMaximumSize(150, 150)
        thumbnail.setPixmap(pixmap)

        return thumbnail

def main() -> None:  
    app = QApplication([])
    window = MainDisplay()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()