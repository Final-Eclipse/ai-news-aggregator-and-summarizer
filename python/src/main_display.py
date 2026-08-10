from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
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

        self.container = QStackedWidget()

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
        """Change the current page of the container to the next."""
        self.current_page_number = self.next_index(reverse=False)
        self._change_page()

    def previous_page(self) -> None:
        """Change the current page of the container to the previous."""
        self.current_page_number = self.next_index(reverse=True)
        self._change_page()

    def _change_page(self) -> None:
        """
        Change the current page of the container.
        
        self.current_page_number increases by 1 because it is initially equal
        to the next valid index. This means that a valid index of 4 would be
        page 5 instead.
        """
        self.container.setCurrentIndex(self.current_page_number)
        self.current_page_number += 1

    def update(self, articles: list) -> None:
        """
        Update main display.

        @param articles: List of articles to create news cards from.
        """
        news_cards: list[QWidget] = self._assemble_news_cards(articles)
        self._add_news_cards_to_container(news_cards)
        
        # Remove landing page.
        if self.landing_page in self.container.children():
            self._remove_landing_page()

    def _add_news_cards_to_container(self, news_cards: list[QWidget]) -> None:
        """
        Add news cards to container.

        @param news_cards: QWidget list of news cards.
        """
        # Create page and add to container.
        for card in news_cards:
            layout = self._create_layout(card)
            page = self._create_page(layout)
            self.container.addWidget(page)

    def _assemble_news_cards(self, articles: list) -> list[QWidget]:
        """
        Assemble news cards into pages.

        @param articles: List of articles.
        @return: QWidget list of pages.
        """
        news_cards = []
        pages = []
        for article in articles[self.article_index:]:
            # Create thumbnail.
            thumbnail_url: str = article[6]
            thumbnail: QLabel = self._create_thumbnail(thumbnail_url)

            # Create description container.
            news_outlet: str = article[1]
            title: str = article[3]
            author: str = article[2]
            desc_container: QWidget = self._create_desc_container(news_outlet, title, author)

            # Create news card.
            news_card: QWidget = self._create_news_card_container(thumbnail, desc_container)
            news_cards.append(news_card)

            if len(news_cards) == self.articles_per_page:
                pages.append(news_cards.copy())
                news_cards.clear()

            # Prevents looping over entire list, which can take a lot of time when the user most likely won't go to the last page anyways.
            if len(pages) == self.pages_to_get:
                break

            self.article_index += 1
        self.article_index += 1

        # If there are still articles left that amount to less than self.articles_per_page, add the rest of them.
        if len(news_cards) > 0:
            pages.append(news_cards.copy())

        return pages

    def next_index(self, reverse: bool) -> int:
        """
        Returns the next/previous valid index position in the QStackedWidget.
        
        @param reverse: Boolean to get the next/previous valid index.
        @return: Integer of the next/previous valid index.
        """
        number_of_children = len(self.container.children()) - 1 # Excludes QStackedLayout.
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

    def _create_page(self, layout: QVBoxLayout) -> QWidget:
        """
        Creates a page that contains a layout with articles.

        @return: QWidget page.
        """
        page = QWidget()
        page.setLayout(layout)
        return page

    def _create_layout(self, news_cards: list) -> QVBoxLayout:
        """
        Creates a layout of news cards.

        @param news_cards: List of news cards.
        @return: QVBoxLayout of news cards.
        """
        layout = QVBoxLayout()
        for card in news_cards:
            layout.addWidget(card)

        return layout

    def _create_news_card_container(self, thumbnail: QLabel, desc_container: QWidget) -> QWidget:
        """
        Creates a news card that contains an article's description and thumbnail.

        @param thumbnail: The picture an article comes with.
        @param desc_container: The description of an article containing the news outlet, title, and author.
        @return: QWidget news card.
        """
        container = QWidget()

        layout = QHBoxLayout()
        layout.addWidget(thumbnail)
        layout.addWidget(desc_container, alignment=Qt.AlignmentFlag.AlignLeft)

        width = int(thumbnail.width() + desc_container.width())
        height = int(thumbnail.height() + desc_container.height())
        
        container.setLayout(layout)
        container.setMaximumSize(width, height)

        return container

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

    def _create_thumbnail(self, url: str) -> QLabel:
        """
        Creates a thumbnail from a URL.

        Some images can produce a warning in the terminal from PyQt5 stating "qt.gui.icc: fromIccProfile: failed minimal tag size sanity."
        This warning is disabled in _disable_icc_warning().

        @param url: Url to convert to bytes.
        @return: QLabel thumbnail image.
        """
        placeholder_thumbnail_path = f"{Path.cwd()}/src/images/placeholder_thumbnail.png"
        pixmap = QPixmap()

        if url == "N/A":
            pixmap.load(placeholder_thumbnail_path)
        else:
            pixmap_data = requests.get(url).content
            if pixmap.loadFromData(pixmap_data) == False:
                pixmap.load(placeholder_thumbnail_path)

        thumbnail = QLabel()
        thumbnail.setScaledContents(True)
        thumbnail.setMaximumSize(150, 150)
        thumbnail.setPixmap(pixmap)
        
        return thumbnail

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

def main() -> None:  
    app = QApplication([])
    window = MainDisplay()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()