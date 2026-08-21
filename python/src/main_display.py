from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable, pyqtSlot, QUrl
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import requests
from pathlib import Path
from PyQt5.QtCore import QLoggingCategory
from news_card import NewsCard
# Queries like "spider man" do not work because there it looks for exact matches.
# Using "spider-man" doesn't work either because the hyphen is removed.

# When the user reaches one to two pages from the last page, start making the next pages and add each new page to the container.
# When the user clicks the search button again, reset self.article_index to 0. This makes it so each search starts from the beginning and not in the middle of the articles list result.
# WHen the user clicks the search button, if there are any pages from the previous search, delete them.

class MainDisplay(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.news_cards = []
        self.finished_news_cards = []

        self.signals = Signals()
        self.signals.news_cards_finished.connect(self._divide_news_cards_into_pages)
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
        self.pages_to_get = 5

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
        if self.current_page_number == self._get_number_of_container_children():
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
        if self._get_number_of_container_children() - 2 <= new_page_index:
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

        self._create_news_cards(self.articles)
        
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

    def _are_news_cards_finished(self) -> None:
        """
        Check if all news cards are finished initializing.
        
        Emit signal when all news cards are finished.
        Do not emit signal if there are threads running.
        Do not emit signal if the number of finished articles does not match the number expected.
        """
        active_thread_count = QThreadPool().globalInstance().activeThreadCount()
        articles_expected: int = self.articles_per_page * self.pages_to_get

        if active_thread_count != 0:
            return
        elif len(self.finished_news_cards) != articles_expected:
            return
        else:
            self.signals.news_cards_finished.emit()

    def _create_news_cards(self, articles: list) -> None:
        """
        Create news cards.

        @param articles: List of articles.
        """
        self.news_cards = []
        for article in articles[self.article_index:]:
            card = NewsCard(article)
            self.news_cards.append(card)

            # Prevents looping over entire list, which can take a lot of time when the user most likely won't go to the last page anyways.
            if len(self.news_cards) == self.pages_to_get * self.articles_per_page:
                break

            self.article_index += 1
        self.article_index += 1

        self.finished_news_cards = []
        for card in self.news_cards:
            card: NewsCard
            card.finished.connect(lambda: self.finished_news_cards.append(card))
            card.finished.connect(self._are_news_cards_finished)
            card.clicked.connect(lambda card_instance: self._create_summary_page(card_instance))

    def _get_number_of_container_children(self) -> int:
        """
        Return number of children widgets in the main display container.

        QStackedLayout is not included in the number of children.

        @return: Number of children widgets.
        """
        return len(self.container.children()) - 1 # Excludes QStackedLayout.

    def _next_index(self, reverse: bool) -> int:
        """
        Return the next/previous valid index position in the QStackedWidget.
        
        @param reverse: Boolean to get the next/previous valid index.
        @return: Integer of the next/previous valid index.
        """
        number_of_children = self._get_number_of_container_children()
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
            news_card: NewsCard
            layout.addWidget(news_card)

        page = QWidget()
        page.setLayout(layout)
        return page

    def _divide_news_cards_into_pages(self) -> None:
        """Split news cards into separate pages."""
        current_page: list[QWidget] = []
        pages: list[list[QWidget]] = []
        for card in self.news_cards:
            current_page.append(card)

            if len(current_page) == self.articles_per_page:
                pages.append(current_page.copy())
                current_page.clear()

        # If there are still articles left that amount to less than self.articles_per_page, add the rest of them.
        if len(current_page) > 0:
            pages.append(current_page.copy())
            current_page.clear()

        self.signals.page_division_finished.emit(pages)

    def _create_summary_page(self, card_instance: NewsCard) -> None:
        summary_container = QWidget()
        summary_container.setStyleSheet("background-color: pink")

        layout = QGridLayout()
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.signals.remove_summary.emit())
        layout.addWidget(back_button, 0, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Load pixmap.
        data = requests.get(card_instance.urlToImage).content
        placeholder_thumbnail_path = f"{Path.cwd()}/src/images/placeholder_thumbnail.png"
        pixmap = QPixmap()
        if data == "N/A":
            pixmap.load(placeholder_thumbnail_path)
        elif pixmap.loadFromData(data) == False:
            pixmap.load(placeholder_thumbnail_path)

        thumbnail = QLabel()
        thumbnail.setPixmap(pixmap)
        layout.addWidget(thumbnail, 1, 0, Qt.AlignmentFlag.AlignCenter)

        name = QLabel(card_instance.name)
        layout.addWidget(name, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        author = QLabel(card_instance.author)
        layout.addWidget(author, 2, 2, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        title = QLabel(card_instance.title)
        layout.addWidget(title, 3, 3, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        description = QLabel(card_instance.description)
        layout.addWidget(description, 4, 4, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        summary_container.setLayout(layout)        
        self.signals.show_summary.emit(summary_container)

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
    news_cards_finished = pyqtSignal()
    page_division_finished = pyqtSignal(list)
    show_summary = pyqtSignal(QWidget)
    remove_summary = pyqtSignal()

def main() -> None:  
    app = QApplication([])
    window = MainDisplay()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()