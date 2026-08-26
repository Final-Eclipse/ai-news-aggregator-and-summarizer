from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
import requests
from pathlib import Path
from news_card import NewsCard

class Summary(QMainWindow):
    back_button_clicked = pyqtSignal()

    def __init__(self, news_card: NewsCard) -> None:
        super().__init__()

        self.id: str = news_card.id
        self.name: str = news_card.name
        self.author: str = news_card.author
        self.title: str = news_card.title
        self.description: str = news_card.description
        self.url: str = news_card.url
        self.urlToImage: str = news_card.urlToImage
        self.publishedAt: str = news_card.publishedAt
        self.content: str = news_card.content

        # self.id: str = "wired"
        # self.name: str = "Wired"
        # self.author: str = "Maxwell Zeff, Lauren Goode, Will Knight"
        # self.title: str = "The White House Is Keeping Its AI Cybersecurity Framework Secret"
        # self.description: str = "The Trump administration shared the details of its plan with OpenAI, Anthropic, and other AI labs on Tuesday. For now, the public remains in the dark."
        # self.url: str = "https://www.wired.com/story/the-white-house-is-keeping-its-ai-cybersecurity-framework-secret/"
        # self.urlToImage: str = "https://media.wired.com/photos/6a7199c152cbcac31bc249b1/191:100/w_1280,c_limit/Trump-Admin-Convenes-AI-Labs-to-Share-AI-Framework-Business-2282299237.jpg"
        # # self.urlToImage: str = "https://preview.redd.it/dead-mans-switch-for-gta-is-insane-v0-7wf0j4iqmwkh1.jpeg?width=1080&crop=smart&auto=webp&s=8c61caa77ea8c78024336158aa79f81f54fb6e90"
        # # self.urlToImage: str = "N/A"
        # self.publishedAt: str = "2026-08-04T22:06:07Z"
        # self.content: str = "The Trump administration has finalized a plan to address the cybersecurity risks posed by increasingly capable artificial intelligence models, a White House official confirmed to WIRED. But at least … [+3676 chars]"

        self.container: QWidget = self._create_summary_page()
        self.setCentralWidget(self.container)

    def _create_summary_page(self) -> QWidget:
        main_container = QWidget()
        main_container.setStyleSheet("background-color: pink")

        # Overall summary page layout = QVBoxLayout
        
        # Back button and title both in first row in a container that has a QGridLayout = container a
        # Use three columns with the third column being empty to push the title to the center
        # Add container a to the overall summary page layout
        
        # Thumbnail, name, author, publishedAt all one container, QVBoxLayout = container b
        # Summary, summarize button all one container, QVBoxLayout = container c
        # Store container b and container c in a container that has a QHBoxLayout = container d
        # Add container d to the overall summary page layout
        
        top_layout = QGridLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.back_button_clicked.emit())
        font = back_button.font()
        font.setPointSize(12)
        font.setFamily("Sitka")
        back_button.setFont(font)
        back_button.setFixedSize(50, 50)
        title = QLabel(self.title)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title.font()
        font.setPointSize(20)
        font.setBold(True)
        font.setFamily("Sitka")
        title.setFont(font)
        top_layout.addWidget(back_button, 0, 0)
        top_layout.addWidget(title, 0, 1)
        placeholder = QWidget()
        placeholder.setFixedSize(back_button.size())
        placeholder.setStyleSheet("background-color: red")
        top_layout.addWidget(placeholder, 0, 2)
        top_container = QWidget()
        top_container.setStyleSheet("background-color: #c19bff")
        top_container.setLayout(top_layout)
        top_container.setFixedHeight(top_container.sizeHint().height())

        thumbnail_layout = QVBoxLayout()
        thumbnail_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        thumbnail_layout.addWidget(self._get_thumbnail())
        thumbnail_layout.addWidget(self._get_details())
        thumbnail_container = QWidget()
        thumbnail_container.setLayout(thumbnail_layout)

        summary_layout = QVBoxLayout()
        summary_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        content_header = QLabel("Content")
        font = content_header.font()
        font.setPointSize(15)
        font.setFamily("Sitka")
        content_header.setFont(font)
        content_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_header.setStyleSheet("background-color: #2bfbc3")
        content_label = QLabel(self.content)
        font = content_label.font()
        font.setPointSize(14)
        font.setFamily("Sitka")
        content_label.setFont(font)
        content_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        content_label.setWordWrap(True)
        content_label.setFixedWidth(600)
        content_label.setFixedHeight(content_label.sizeHint().height())
        content_label.setStyleSheet("background-color: #ff4a89")
        summary_header = QLabel("Summary")
        summary_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = summary_header.font()
        font.setPointSize(15)
        font.setFamily("Sitka")
        summary_header.setFont(font)
        summary_header.setStyleSheet("background-color: #c92bfb")
        summary_label = QLabel()
        summary_label.setFixedSize(content_label.width(), 600)
        summary_label.setStyleSheet("background-color: #9bcbff")

        summary_button = QPushButton("Summarize")
        font = summary_button.font()
        font.setPointSize(15)
        font.setFamily("Sitka")
        summary_button.setFont(font)
        summary_button.setFixedSize(100, 50)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(summary_button)
        button_container = QWidget()
        button_container.setFixedWidth(content_label.width())
        button_container.setStyleSheet("background-color: #9bffff")
        button_container.setLayout(button_layout)

        summary_layout.addWidget(content_header)
        summary_layout.addWidget(content_label)
        summary_layout.addWidget(summary_header)
        summary_layout.addWidget(summary_label)
        summary_layout.addWidget(button_container)
        summary_container = QWidget()
        summary_container.setLayout(summary_layout)

        thumbnail_summary_layout = QHBoxLayout()
        thumbnail_summary_layout.addWidget(thumbnail_container)
        thumbnail_summary_layout.addWidget(summary_container)
        thumbnail_summary_container = QWidget()
        thumbnail_summary_container.setLayout(thumbnail_summary_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(top_container)
        main_layout.addWidget(thumbnail_summary_container)

        main_container.setLayout(main_layout)        
        return main_container

    def _get_thumbnail(self) -> QLabel:
        # Load pixmap.
        placeholder_thumbnail_path = f"{Path.cwd()}/src/images/placeholder_thumbnail.png"
        pixmap = QPixmap()
        if self.urlToImage == "N/A":
            pixmap.load(placeholder_thumbnail_path)
        else: 
            data = requests.get(self.urlToImage).content
            if pixmap.loadFromData(data) == False:
                pixmap.load(placeholder_thumbnail_path)

        thumbnail = QLabel()
        thumbnail.setScaledContents(True)
        thumbnail.setPixmap(pixmap)
        return thumbnail

    def _get_details(self) -> QLabel:
        details = QLabel(f"{self.name}\n{self.author}\n{self.publishedAt}")
        font = details.font()
        font.setPointSize(14)
        font.setFamily("Sitka")
        details.setFont(font)
        details.setStyleSheet("background-color: yellow")
        details.setAlignment(Qt.AlignmentFlag.AlignTop)
        details.setFixedSize(details.sizeHint().width(), details.sizeHint().height())
        return details

def main() -> None:  
    app = QApplication([])
    window = Summary()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()