from PyQt5.QtWidgets import QApplication, QComboBox, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QSizePolicy, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import QObject, QSize, QThread, QThreadPool, Qt, pyqtSignal, QRunnable
from PyQt5.QtGui import QFontMetrics, QFont
from services.worker import *
from endpoints import Everything, TopHeadlines, Sources

"""
# Make post request to Java using the URL.
# Or have Java make the post request as well without doing it in Python and just return the JSON.

# Make request to URL in Python or Java and save the JSON.
# For every entry in the JSON, display it on the app.

# Most likely use Python because the JSON will be needed to store the articles in the database.
# Also, what would Java be doing? Python needs to iterate over each article to get the image, url, etc.
# Java wouldn't really be doing anything.

# Use URL to send to Java getEverythingResponse() and get the JSON result.
# Save the JSON to the database.
# Display articles in the app based on details and information provided in the JSON.
# getEverythingResponse() unnecessary? Just use Python to make a GET request instead of doing it in Java.
# Probably should just do it in Java since I already have the URL so I can just do everything in Java first without needed Python to do extra stuff.

# When an article is clicked on, perhaps display the original full article.
# Have a summarize button to summarize the article.
# Display the summary.
"""

class TopBar(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.everything = Everything()
        self.top_headlines = TopHeadlines()
        self.sources = Sources()

        self.endpoint_selector: QComboBox = self._create_endpoint_selector()
        self.endpoint_selector.currentIndexChanged.connect(self._update_top_bar)

        self.container: QWidget = self._create_layout()

        # Initialized in self._store_database_results().
        self.database_results: list

        self.setWindowTitle("")
        self.setCentralWidget(self.container)

    @pyqtSlot(dict)
    def save_articles_to_database(self, response: dict) -> None:
        """
        Save articles to database after the endpoint response is received.
        
        @param response: Dictionary object of the endpoint response received in _get_endpoint_response().
        """
        endpoint_type, json_str = self._get_endpoint_data()

        threadpool = QThreadPool().globalInstance()
        worker = DatabaseWorker(endpoint_type, response)
        worker.signal.articles_saved.connect(self._get_database_results)
        threadpool.start(worker)
        # Make sure to grab all results when fetching calling News API.
        # Grab each page of the JSON result, not just the first page.
        # page=1, page=2, page=3, etc.
        # Uses too many API calls to do this.
        # Instead, when the user clicks to the next page, call the same endpoint URL with News API, but page = next page.

        # Emit signal to main_display.py to notify it to update the screen with articles.

    @pyqtSlot()
    def _get_endpoint_response(self) -> None:
        """Get the response of the endpoint URL posted earlier in _post_endpoint_data."""
        endpoint_type, json_str = self._get_endpoint_data()

        threadpool = QThreadPool().globalInstance()
        worker = EndpointResponseWorker(endpoint_type)
        worker.signal.response_finished.connect(lambda response: self.save_articles_to_database(response))
        threadpool.start(worker)

    @pyqtSlot()
    def _post_endpoint_data(self) -> None:
        """Post endpoint data from which the endpoint URL is able to be constructed."""
        endpoint_type, json_str = self._get_endpoint_data()

        threadpool = QThreadPool().globalInstance()

        worker = EndpointDataWorker()
        worker.set_query_parameters(json_str)
        worker.signal.upload_finished.connect(self._get_endpoint_response)

        threadpool.start(worker)
    
    def _get_endpoint_data(self) -> tuple:
        """
        Get the current endpoint and the information to assemble its endpoint URL.
        
        @return: Tuple of the current endpoint and its JSON string.
        """
        endpoint_type = self.endpoint_selector.currentText().lower().replace(" ", "-")
        
        match endpoint_type:
            case "everything":
                json_str = self.everything.get_json(endpoint_type)
            case "top-headlines":
                json_str = self.top_headlines.get_json(endpoint_type)
            case "sources":
                endpoint_type = "top-headlines/sources"
                json_str = self.sources.get_json(endpoint_type)
            case _:
                raise Exception("[_get_endpoint_data() in top_bar.py] Endpoint type not selected.")

        return endpoint_type, json_str

    def get_container(self) -> QWidget:
        """
        Return the container for the top bar.

        @return: QWidget.
        """
        return self.container

    def _update_top_bar(self) -> None:   
        """Update the top bar by showing and hiding elements."""
        match self.endpoint_selector.currentText():
            case "Everything":
                self.everything.show()
                self.top_headlines.hide()
                self.sources.hide()
                self.placeholder.hide()

            case "Top headlines":
                self.everything.hide()
                self.top_headlines.show()
                self.sources.hide()
                self.placeholder.hide()

            case "Sources":
                self.everything.hide()
                self.top_headlines.hide()
                self.sources.show()
                self.placeholder.hide()

            case _:
                self.everything.hide()
                self.top_headlines.hide()
                self.sources.hide()
                self.placeholder.show()

    def _create_layout(self) -> QWidget:
        """
        Create the layout for the top bar.

        @return: QWidget container for the top bar.
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)

        layout.addWidget(self._create_endpoint_selector_container())
        
        layout.addWidget(self.everything.container)
        layout.addWidget(self.top_headlines.container)
        layout.addWidget(self.sources.container)
        layout.addWidget(self._create_placeholder())

        # Move create container into separate method.
        self.container = QWidget()  # Make into an instance variable.
        # self.container.setStyleSheet(f"background-color: #eeeeee")
        # self.container.setStyleSheet(f"background-color: #D0D0D0")
        self.container.setLayout(layout)
        # fixed_height = int(self.screen().size().height() * 0.12)
        fixed_height = int(self.container.sizeHint().height() * 1.65)   # Works differently on different devices. 
        self.container.setFixedHeight(fixed_height)
        
        return self.container
    
    def _create_placeholder(self) -> QWidget:
        """
        Create a placeholder widget that is shown when no endpoint is chosen in the endpoint selector.
        
        Blocks the second row in the container when the default dropdown option is selected.
        Prevents the lower rows from moving upwards.
        
        @return: QWidget placeholder.
        """
        self.placeholder = QWidget()
        return self.placeholder
    
    def _create_endpoint_selector(self) -> QComboBox:
        """
        Create endpoint selector that allows the user to switch between various endpoints.

        @return: QComboBox of endpoints.
        """
        endpoint_selector = QComboBox()        
        endpoint_selector.addItems(["Select an endpoint type", "Everything", "Top headlines", "Sources"])

        max_width = endpoint_selector.sizeHint().width()
        endpoint_selector.setMaximumWidth(max_width)

        return endpoint_selector

    def _create_search_button(self) -> QPushButton:
        """
        Creates a search button.
        
        @return: QPushButton.
        """
        search_button = QPushButton("Search")
        search_button.clicked.connect(self._post_endpoint_data)

        max_width = search_button.sizeHint().width()
        search_button.setMaximumWidth(max_width)
        return search_button

    @pyqtSlot()
    def _get_database_results(self) -> None:
        """Get database results based off of bindings/user input from the endpoint selector."""
        # Get database bindings.
        bindings: dict
        current_endpoint = endpoint_type = self.endpoint_selector.currentText().lower().replace(" ", "-")
        match current_endpoint:
            case "everything":
                bindings = self.everything.get_database_bindings(current_endpoint)
            case "top-headlines":
                bindings = self.top_headlines.get_database_bindings(current_endpoint)
            case "sources":
                bindings = self.sources.get_database_bindings(current_endpoint)
            case _:
                pass

        # Query database.
        threadpool = QThreadPool().globalInstance()
        worker = DatabaseQueryWorker(endpoint_type, bindings)
        worker.signal.query_finished.connect(self._store_database_results)
        threadpool.start(worker)

    @pyqtSlot(list)
    def _store_database_results(self, results: list) -> None:
        self.database_results = results
        print(self.database_results)
        print(len(self.database_results))
                
    def _create_endpoint_selector_container(self) -> QWidget:
        """
        Creates a container made up of the endpoint selector and search button.
        
        @return: QWidget container.
        """
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        label = QLabel("Endpoint type")
        label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(label, 0, 0)

        layout.addWidget(self.endpoint_selector, 1, 0)
        layout.addWidget(self._create_search_button(), 1, 1)

        container = QWidget()
        container.setLayout(layout)
        
        return container
    
def main() -> None:  
    app = QApplication([])
    window = TopBar()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()