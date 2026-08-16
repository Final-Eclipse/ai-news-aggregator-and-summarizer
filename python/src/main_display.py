from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable, pyqtSlot, QUrl
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import requests
from pathlib import Path
from PyQt5.QtCore import QLoggingCategory

# Queries like "spider man" do not work because there it looks for exact matches.
# Using "spider-man" doesn't work either because the hyphen is removed.

# When the user reaches one to two pages from the last page, start making the next pages and add each new page to the container.
# When the user clicks the search button again, reset self.article_index to 0. This makes it so each search starts from the beginning and not in the middle of the articles list result.
# WHen the user clicks the search button, if there are any pages from the previous search, delete them.

class MainDisplay(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.signals = Signals()
        self.signals.thumbnails_finished.connect(lambda thumbnails: self._create_news_card_containers(thumbnails))
        self.signals.news_cards_finished.connect(lambda news_cards: self._divide_news_cards_into_pages(news_cards))
        self.signals.page_division_finished.connect(lambda pages: self._add_pages_to_container(pages))

        self.container = QStackedWidget()
        self.desc_containers: list[QWidget]

        self.landing_page: QLabel
        self._init_landing_page()
        
        # Index position within the database query.
        self.article_index = 0

        # Number of articles to display per page.
        self.articles_per_page = 4

        # Number of pages to get at one time.
        self.pages_to_get = 2

        # The current page number the user is on.
        self.current_page_number = 1
        
        self._disable_icc_warning()
        self.setCentralWidget(self.container)

    def _init_landing_page(self) -> None:
        """Initialize the landing page of the container."""
        self.landing_page = QLabel("Use the inputs above to search for news articles.")
        self.landing_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container.addWidget(self.landing_page)
        self.container.setStyleSheet("background-color: pink;")

    def _remove_landing_page(self) -> None:
        """Remove the landing page of the container."""
        self.container.removeWidget(self.landing_page)
        self.landing_page.deleteLater()

    def next_page(self) -> None:
        """
        Change the current page of the container to the next.
        
        Does not move from the last page to the first page.
        """
        if self.current_page_number == self._get_container_children():
            return
        
        self._change_page(self._next_index(reverse=False))

    def previous_page(self) -> None:
        """
        Change the current page of the container to the previous.
        
        Does not move from the first page to the last page.
        """
        if self.current_page_number == 1:
            return
        
        self._change_page(self._next_index(reverse=True))

    def _change_page(self, new_page_index: int) -> None:
        """
        Change the current page of the container.
        
        self.current_page_number increases by 1 because it is initially equal
        to the next valid index. This means that a valid index of 4 would be
        page 5 instead.

        Also creates more pages if the user reaches near the end of what is 
        currently available.

        @param new_page_number: Integer value of the new page index.
        """
        self.container.setCurrentIndex(new_page_index)
        
        # Create more pages if current page reaches a certain number.
        if self._get_container_children() - 2 <= new_page_index:
            self.update(reset_pages=False)

        self.current_page_number = new_page_index + 1
        self.signals.page_changed.emit(self.current_page_number)

    def update(self, reset_pages: bool) -> None:
        """
        Update main display.

        @param reset_pages: Delete previous pages and reset article index if true.
        """
        if reset_pages == True:
            self._delete_previous_pages()

        self._get_thumbnails_urls_and_descs(self.articles)
        
        # Remove landing page.
        if self.landing_page in self.container.children():
            self._remove_landing_page()

    def _delete_previous_pages(self) -> None:
        """Delete all previous pages in the main display container."""
        self.article_index = 0
        for page in self.container.children():
            if type(page) == QWidget:
                self._change_page(0)
                self.container.removeWidget(page)
                page.deleteLater()

    def _set_articles(self, articles: list) -> None:
        """
        Set articles to parameter.

        @param articles: List of articles.
        """
        self.articles = articles

    def _add_pages_to_container(self, pages: list[list[QWidget]]) -> None:
        """
        Add pages to container.

        @param pages: List of QWidget lists of pages.
        """
        for page in pages:
            page_container: QWidget = self._create_page_container(page)
            self.container.addWidget(page_container)

    def _get_thumbnails_urls_and_descs(self, articles: list) -> None:
        """
        Get thumbnail URLs and create description containers.

        @param articles: List of articles.
        """
        desc_containers = []
        thumbnail_urls = []
        for article in articles[self.article_index:]:
            # Get thumbnail urls.
            thumbnail_url: str = article[6]
            thumbnail_urls.append(thumbnail_url)

            # Create description container.
            news_outlet: str = article[1]
            title: str = article[3]
            author: str = article[2]
            desc_container: QWidget = self._create_desc_container(news_outlet, title, author)
            desc_containers.append(desc_container)

            # Prevents looping over entire list, which can take a lot of time when the user most likely won't go to the last page anyways.
            if len(desc_containers) == self.pages_to_get * self.articles_per_page:
                self.desc_containers = desc_containers
                break

            self.article_index += 1
        self.article_index += 1

        self._convert_thumbnails_to_bytes(thumbnail_urls)

    def _convert_thumbnails_to_bytes(self, thumbnail_urls: list[str]) -> None: 
        """
        Convert all given thumbnail URLs to their bytes form.

        Create threads within QThreadPool to asynchronously make HTTP requests to gather
        bytes data without disrupting the main GUI thread.

        @param thumbnail_urls: List of URLs that direct to an article's thumbnail.
        """
        list_size = len(thumbnail_urls)
        handler = ThumbnailHandler(list_size)
        handler.signal.threads_finished.connect(lambda bytes_data: self._create_thumbnails(bytes_data))

        for index_position, url in enumerate(thumbnail_urls):
            threadpool = QThreadPool().globalInstance()
            worker = ThumbnailWorker(url, index_position)
            worker.signal.non_bytes_finished.connect(lambda data, pos: handler._handle_thumbnail_urls(data, pos))
            worker.signal.bytes_finished.connect(lambda data, pos: handler._handle_thumbnail_urls(data, pos))
            threadpool.start(worker)

    def _get_container_children(self) -> int:
        """
        Return number of children widgets in the main display container.

        QStackedLayout is not included in the number of children.

        @return: Number of children widgets.
        """
        return len(self.container.children()) - 1 # Excludes QStackedLayout.

    def _next_index(self, reverse: bool) -> int:
        """
        Returns the next/previous valid index position in the QStackedWidget.
        
        @param reverse: Boolean to get the next/previous valid index.
        @return: Integer of the next/previous valid index.
        """
        number_of_children = self._get_container_children()
        current_index = self.container.currentIndex()
        next_index = 0

        if reverse == False:    
            if current_index == number_of_children - 1:
                next_index = 0
            else:
                next_index = current_index + 1

        elif reverse == True:
            if current_index == 0:
                next_index = number_of_children - 1
            else:
                next_index = current_index - 1
        
        return next_index

    def _create_page_container(self, page: list[QWidget]) -> QWidget:
        """
        Create a page that contains a layout with articles.

        @return: QWidget page.
        """
        layout = QVBoxLayout()
        for news_card in page:
            layout.addWidget(news_card)

        page = QWidget()
        page.setLayout(layout)
        return page

    def _divide_news_cards_into_pages(self, news_cards: list[QWidget]) -> None:
        current_page: list[QWidget] = []
        pages: list[list[QWidget]] = []
        for news_card in news_cards:
            current_page.append(news_card)

            if len(current_page) == self.articles_per_page:
                pages.append(current_page.copy())
                current_page.clear()

        # If there are still articles left that amount to less than self.articles_per_page, add the rest of them.
        if len(current_page) > 0:
            pages.append(current_page.copy())
            current_page.clear()
        
        self.signals.page_division_finished.emit(pages)

    def _create_news_card_containers(self, thumbnails: list[QLabel]) -> None:
        """
        Create news cards that contain an article's description and thumbnail.

        @param thumbnails: The picture an article comes with.
        """
        news_cards: list[QWidget] = []
        for x in range(0, len(thumbnails)):
            container = QWidget()

            layout = QHBoxLayout()
            layout.addWidget(thumbnails[x])
            layout.addWidget(self.desc_containers[x], alignment=Qt.AlignmentFlag.AlignLeft)

            width = int(thumbnails[x].width() + self.desc_containers[x].width())
            height = int(thumbnails[x].height() + self.desc_containers[x].height())
            
            container.setLayout(layout)
            container.setMaximumSize(width, height)

            news_cards.append(container)

        self.signals.news_cards_finished.emit(news_cards)

    def _create_desc_container(self, news_outlet: str, title: str, author: str) -> QWidget:
        """
        Creates a description container of various details about an article.

        @param news_outlet: News outlet that published the article.
        @param title: Name of the article.
        @param author: The writer of the article.
        @return: QWidget description container.
        """
        container = QWidget()
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        row = 0
        col = 0
        news_outlet = self._create_label(news_outlet)
        layout.addWidget(news_outlet, row, col, alignment=Qt.AlignmentFlag.AlignLeft)

        row += 1
        title = self._create_label(title)
        layout.addWidget(title, row, col)

        row += 1
        author = self._create_label(author)
        layout.addWidget(author, row, col, alignment=Qt.AlignmentFlag.AlignRight)

        container.setLayout(layout)

        offset = 1.2
        width = int(layout.sizeHint().width() * offset)
        height = int(layout.sizeHint().height() * offset)
        container.setMaximumSize(width, height)
        
        return container

    def _create_thumbnails(self, bytes_data: list[bytes|str]) -> None:
        """
        Create pixmaps and apply to thumbnails.

        Some images can produce a warning in the terminal from PyQt5 stating "qt.gui.icc: fromIccProfile: failed minimal tag size sanity."
        This warning is disabled in _disable_icc_warning().

        @param bytes_data: List of bytes or str for every article's thumbnail.
        """
        thumbnails = []
        placeholder_thumbnail_path = f"{Path.cwd()}/src/images/placeholder_thumbnail.png"
        for data in bytes_data:
            pixmap = QPixmap()

            if data == "N/A":
                pixmap.load(placeholder_thumbnail_path)
            elif pixmap.loadFromData(data) == False:
                pixmap.load(placeholder_thumbnail_path)

            thumbnail = QLabel()
            thumbnail.setScaledContents(True)
            thumbnail.setMaximumSize(150, 150)
            thumbnail.setPixmap(pixmap)

            thumbnails.append(thumbnail)    
        
        self.signals.thumbnails_finished.emit(thumbnails)

    def _create_label(self, text: str) -> QLabel:
        """
        Creates a label that displays test.

        @param text: String of characters to display on the label.
        @return: QLabel.
        """
        label = QLabel(text)
        label.setMaximumSize(label.sizeHint().width(), label.sizeHint().height())
        return label

    def _disable_icc_warning(self) -> None:
        """Disable warning when loading image with an incorrect ICC color profile."""
        QLoggingCategory.setFilterRules("qt.gui.icc.warning=false\n")

    def closeEvent(self, a0):
        """Remove any unstarted runnables from the QThreadPool queue on application close."""
        QThreadPool().globalInstance().clear()
        return super().closeEvent(a0)

class Signals(QObject):
    # Pagination
    page_changed = pyqtSignal(int)

    # Update GUI
    thumbnails_finished = pyqtSignal(list)
    news_cards_finished = pyqtSignal(list)
    page_division_finished = pyqtSignal(list)

class ThumbnailHandler():
    def __init__(self, list_size: int) -> None:
        """
        @param max_size: List size to be used to hold the incoming bytes.
        """
        self.signal = ThumbnailSignals()
        self.all_bytes_data = [None] * list_size
        
    def _handle_thumbnail_urls(self, bytes_data: bytes, index_position: int) -> None:
        """
        Store incoming bytes in a list and emit when there are no more active threads.
        
        @param bytes_data: Incoming bytes to be appended to this instance's list.
        @param index_position: Position the bytes should appear in the list.
        """
        self.all_bytes_data[index_position] = bytes_data

        active_thread_count = QThreadPool().globalInstance().activeThreadCount()        
        if active_thread_count == 0:
            self.signal.threads_finished.emit(self.all_bytes_data)

class ThumbnailWorker(QRunnable):
    def __init__(self, url: str, index_position: int) -> None:
        """
        @param url: Thumbnail URL.
        @param index_position: Position the URL appears in the list.
        """
        super().__init__()
        self.signal = ThumbnailSignals()
        self.url = url
        self.index_position = index_position

    @pyqtSlot()
    def run(self) -> None:
        """
        Make HTTP request to URL and emit the response as bytes.
        
        Invalid URLs are emitted immediately without any request.
        
        Long requests timeout after a given amount of time.
        """
        if self.url == "N/A":
            self.signal.non_bytes_finished.emit(self.url, self.index_position)
        else:
            try:
                bytes_data = requests.get(self.url, timeout=1).content
                self.signal.bytes_finished.emit(bytes_data, self.index_position)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                self.signal.non_bytes_finished.emit("N/A", self.index_position)

class ThumbnailSignals(QObject):
    # ThumbnailHandler
    threads_finished = pyqtSignal(list)

    # ThumbnailWorker
    bytes_finished = pyqtSignal(bytes, int)
    non_bytes_finished = pyqtSignal(str, int)

def main() -> None:  
    app = QApplication([])
    window = MainDisplay()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()