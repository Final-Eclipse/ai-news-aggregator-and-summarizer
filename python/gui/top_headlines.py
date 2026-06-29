from PyQt5.QtWidgets import QComboBox, QWidget, QLineEdit, QGridLayout
from endpoint import Endpoint
from helpers import Category, Country

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
            "q": QLineEdit(),
            "pageSize": QLineEdit(),
            "page": QLineEdit()
        }

        return parameters
    
    def _init_fields(self) -> None:
        parameters = self.parameters

        country: QComboBox = parameters["country"]
        country.addItems(Country.qcombobox_options)

        category: QComboBox = parameters["category"]
        category.addItems(Category.qcombobox_options)

        sources: QComboBox = parameters["sources"]
        sources.addItems(["Select source(s)", "ABC News", "Associated Press"])

        q: QLineEdit = parameters["q"]
        q.setPlaceholderText("Type query")

        pageSize: QLineEdit = parameters["pageSize"]
        pageSize.setPlaceholderText("Type page size")

        page: QLineEdit = parameters["page"]
        page.setPlaceholderText("Type page number")