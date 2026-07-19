from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
import requests

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
        label.setMaximumSize(label.sizeHint().width(), label.sizeHint().height())
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
        layout.addWidget(brief_desc, row, col)

        row += 1
        author = self._create_label("AP")
        layout.addWidget(author, row, col, alignment=Qt.AlignmentFlag.AlignRight)

        container.setLayout(layout)

        offset = 1.2
        width = int(layout.sizeHint().width() * offset)
        height = int(layout.sizeHint().height() * offset)
        container.setMaximumSize(width, height)
        
        return container
    
    def create_news_container(self) -> QWidget:
        container = QWidget()
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
        container.setMaximumSize(width, height)

        return container
    
    def _create_thumbnail(self) -> QLabel:
        pixmap_data = requests.get(f"https://dims.apnews.com/dims4/default/c922f70/2147483647/strip/true/crop/4032x2687+0+1/resize/980x653!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Fb5%2F7a%2Ff984fedcb9c5272fd78048480f94%2F465bab7e3f944edeab2dd60412faf0db").content

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