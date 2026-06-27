from PyQt5.QtWidgets import QComboBox, QWidget, QLineEdit, QGridLayout
from endpoint import Endpoint

class TopHeadlines(Endpoint):
    def __init__(self) -> None:
        self.parameters: dict = self.init_parameters()

        self.layout: QGridLayout = self._create_layout()
        self.container: QWidget = self._create_container(self.layout)

        self._init_fields()
        self._init_widget_sizes()

        self.hide()

    def init_parameters(self) -> dict:
        parameters = {
            "country": QComboBox(),
            "category": QComboBox(),
            "sources": QComboBox(),
            "query": QLineEdit(),
            "pageSize": QLineEdit(),
            "page": QLineEdit()
        }

        return parameters
    
    def _init_fields(self) -> None:
        parameters = self.parameters

        country: QComboBox = parameters["country"]
        country.addItems(["Select country", "United States", "Canada", "Mexico"])

        category: QComboBox = parameters["category"]
        category.addItems(["Select category", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])

        sources: QComboBox = parameters["sources"]
        sources.addItems(["Select source(s)", "ABC News", "Associated Press"])

        query: QLineEdit = parameters["query"]
        query.setPlaceholderText("Type query")

        pageSize: QLineEdit = parameters["pageSize"]
        pageSize.setPlaceholderText("Type page size")

        page: QLineEdit = parameters["page"]
        page.setPlaceholderText("Type page number")