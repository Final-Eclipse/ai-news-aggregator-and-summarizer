from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit, QStackedWidget
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap
import requests
from pathlib import Path
from PyQt5.QtCore import QLoggingCategory

# Queries like "spider man" do not work because there it looks for exact matches.
# Using "spider-man" doesn't work either because the hyphen is removed.

class MainDisplay(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.container = QStackedWidget()
        self._init_landing_page()

        # Index position within the database query.
        self.article_index = 0

        # Number of articles to display per page.
        self.articles_per_page = 4

        # Number of pages to get at one time.
        self.pages_to_get = 5

        # The current page number the user is on.
        self.current_page_number: int
        
        self._disable_icc_warning()
        self.setCentralWidget(self.container)

    def _init_landing_page(self) -> None:
        """Initializes the first page of the container."""
        first_page = QLabel("Use the inputs above to search for news articles.")
        first_page.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container.addWidget(first_page)
        self.container.setStyleSheet("background-color: pink;")

    def next_page(self) -> None:
        """Changes the current page on the container to the next."""
        self.current_page_number = self.next_index(reverse=False)
        self.container.setCurrentIndex(self.current_page_number)

    def previous_page(self) -> None:
        """Changes the current page on the container to the previous."""
        self.current_page_number = self.next_index(reverse=True)
        self.container.setCurrentIndex(self.current_page_number)

    def update(self, articles: list) -> None:
        """
        Create pages to view.

        @param articles: List of articles to create news cards from.
        """
        news_cards = []
        current_page = []
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
            news_card: QWidget = self._create_news_card(thumbnail, desc_container)
            current_page.append(news_card)

            if len(current_page) == self.articles_per_page:
                news_cards.append(current_page.copy())
                current_page.clear()

            # Prevents looping over entire list, which can take a lot of time when the user most likely won't go to the last page anyways.
            if len(news_cards) == self.pages_to_get:
                break

            self.article_index += 1

        # If there are still articles left that amount to less than self.articles_per_page, add the rest of them.
        if len(current_page) > 0:
            news_cards.append(current_page.copy())

        self.article_index += 1

        # Create page and add to container.
        for card in news_cards:
            layout = self._create_layout(card)
            page = self._create_page(layout)
            self.container.addWidget(page)

        self.next_page()

    def next_index(self, reverse: bool):
        """Returns the next valid index position in the QStackedWidget."""
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

    def _create_news_card(self, thumbnail: QLabel, desc_container: QWidget) -> QWidget:
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