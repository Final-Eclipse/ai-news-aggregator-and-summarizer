from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QObject, QThreadPool, Qt, pyqtSignal, QRunnable, pyqtSlot
from PyQt5.QtGui import QPixmap
import requests
from pathlib import Path

class NewsCard(QWidget):
    pixmap_created = pyqtSignal(QPixmap)
    thumbnail_finished = pyqtSignal()
    layout_set = pyqtSignal()
    finished = pyqtSignal()
    clicked = pyqtSignal(object)

    def __init__(self, article: list[str]) -> None:
        super().__init__()

        self.id: str = article["source"]["id"]
        self.name: str = article["source"]["name"]
        self.author: str = article["author"]
        self.title: str = article["title"]
        self.description: str = article["description"]
        self.url: str = article["url"]
        self.urlToImage: str = article["urlToImage"]
        self.publishedAt: str = article["publishedAt"]
        self.content: str = article["content"]

        # self.id: str = article[0]        
        # self.name: str = article[1]        
        # self.author: str = article[2]        
        # self.title: str = article[3]        
        # self.description: str = article[4]        
        # self.url: str = article[5]        
        # self.urlToImage: str = article[6]        
        # self.publishedAt: str = article[7]
        # self.content: str = article[8]

        self.desc_container = self._create_desc_container()

        self._convert_thumbnail_to_bytes()
        self.pixmap_created.connect(self._create_thumbnail)
        self.thumbnail: QLabel

        self.thumbnail_finished.connect(self._create_layout)
        self.layout_set.connect(self.finished.emit)

    def _create_label(self, text: str) -> QLabel:
        """
        Create a label that displays text.

        @param text: String of characters to display on the label.
        @return: QLabel.
        """
        label = QLabel(text)
        label.setMaximumSize(label.sizeHint().width(), label.sizeHint().height())
        return label
        
    def _create_desc_container(self) -> QWidget:
        """
        Create a description container of various details about an article.

        @return: QWidget description container.
        """
        desc_container = QWidget()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        row = 0
        col = 0
        news_outlet = self._create_label(self.name)
        layout.addWidget(news_outlet, row, col, alignment=Qt.AlignmentFlag.AlignLeft)

        row += 1
        title = self._create_label(self.title)
        layout.addWidget(title, row, col)

        row += 1
        author = self._create_label(self.author)
        layout.addWidget(author, row, col, alignment=Qt.AlignmentFlag.AlignRight)

        desc_container.setLayout(layout)

        offset = 1.2
        width = int(layout.sizeHint().width() * offset)
        height = int(layout.sizeHint().height() * offset)
        desc_container.setMaximumSize(width, height)
        
        return desc_container

    def _convert_thumbnail_to_bytes(self) -> None: 
        """Make a HTTP request to self.urlToImage and get its representation in bytes."""
        threadpool = QThreadPool().globalInstance()
        worker = ThumbnailWorker(self.urlToImage)
        worker.signal.non_bytes_finished.connect(self._create_pixmap)
        worker.signal.bytes_finished.connect(self._create_pixmap)
        threadpool.start(worker)

    def _create_pixmap(self, byte_data: bytes|str) -> None:
        """
        Create pixmap and emit as a signal.

        Some images can produce a warning in the terminal from PyQt5 stating "qt.gui.icc: fromIccProfile: failed minimal tag size sanity."
        This warning is disabled in MainDisplay._disable_icc_warning().

        @param byte_data: List of bytes or str for every article's thumbnail.
        """
        placeholder_thumbnail_path = f"{Path.cwd()}/src/images/placeholder_thumbnail.png"
        pixmap = QPixmap()

        if byte_data == "N/A":
            pixmap.load(placeholder_thumbnail_path)
        elif pixmap.loadFromData(byte_data) == False:
            pixmap.load(placeholder_thumbnail_path)

        self.pixmap_created.emit(pixmap)

    def _create_thumbnail(self, pixmap: QPixmap) -> None:
        """
        Create thumbnail and apply pixmap.

        @param pixmap: QPixmap image.
        """
        thumbnail = QLabel()
        thumbnail.setScaledContents(True)
        thumbnail.setMaximumSize(150, 150)
        thumbnail.setPixmap(pixmap)

        self.thumbnail = thumbnail
        self.thumbnail_finished.emit()

    def _create_layout(self) -> None:
        """Create and set the layout for the news card."""
        layout = QHBoxLayout()
        layout.addWidget(self.thumbnail)
        layout.addWidget(self.desc_container, alignment=Qt.AlignmentFlag.AlignLeft)

        width = int(self.thumbnail.width() + self.desc_container.width())
        height = int(self.thumbnail.height() + self.desc_container.height())

        self.setLayout(layout)
        self.setMaximumSize(width, height)

        self.layout_set.emit()

    def mousePressEvent(self, a0):
        self.clicked.emit(self)
        return super().mousePressEvent(a0)

class ThumbnailWorker(QRunnable):
    def __init__(self, url: str) -> None:
        """
        @param url: Thumbnail URL.
        """
        super().__init__()
        self.signal = ThumbnailSignals()
        self.url = url

    @pyqtSlot()
    def run(self) -> None:
        """
        Make HTTP request to URL and emit the response as bytes.
        
        Invalid URLs are emitted immediately without any request.
        
        Long requests timeout after a given amount of time.
        """
        if self.url == "N/A":
            self.signal.non_bytes_finished.emit(self.url)
        else:
            try:
                byte_data = requests.get(self.url, timeout=1).content
                self.signal.bytes_finished.emit(byte_data)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                self.signal.non_bytes_finished.emit("N/A")

class ThumbnailSignals(QObject):
    bytes_finished = pyqtSignal(bytes)
    non_bytes_finished = pyqtSignal(str)