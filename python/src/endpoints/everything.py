from PyQt5.QtWidgets import QComboBox, QWidget, QLineEdit, QGridLayout
from endpoints.endpoint import Endpoint
from endpoints.helpers import Language, Domains, Sources

class Everything(Endpoint):
    def __init__(self) -> None:
        self.parameters: dict = self._init_parameters()
        
        self.layout: QGridLayout = self._create_layout()
        self.container: QWidget = self._create_container(self.layout)

        self._init_fields()
        self._init_widget_sizes()

        self.hide()

    def _init_parameters(self) -> dict:
        parameters = {
            "q": QLineEdit(),
            "searchIn": QComboBox(),  
            "sources": QComboBox(),
            "domains": QComboBox(),
            "excludeDomains": QComboBox(),
            "from": QLineEdit(),
            "to": QLineEdit(),
            "language": QComboBox(),
            # "sortBy": QComboBox(),
            # "pageSize": QLineEdit(),
            # "page": QLineEdit()
        }

        return parameters            
    
    def _init_fields(self) -> None:
        parameters = self.parameters

        q: QLineEdit = parameters["q"]
        q.setPlaceholderText("Type query")

        searchIn: QComboBox = parameters["searchIn"]
        searchIn.addItems(["Select search type(s)", "Title", "Description", "Content"])

        sources: QComboBox = parameters["sources"]
        sources.addItems(Sources.qcombobox_options)

        domains: QComboBox = parameters["domains"]
        domains.addItems(Domains.qcombobox_options)

        excludeDomains: QComboBox = parameters["excludeDomains"]
        excludeDomains.addItems(Domains.qcombobox_options)

        from_: QLineEdit = parameters["from"]
        from_.setPlaceholderText("Type start date")

        to: QLineEdit = parameters["to"]
        to.setPlaceholderText("Type end date")

        language: QComboBox = parameters["language"]
        language.addItems(Language.qcombobox_options)

        # sortBy: QComboBox = parameters["sortBy"]
        # sortBy.addItems(["Select sort option", "Relevancy", "Popularity", "Date published"])

        # pageSize: QLineEdit = parameters["pageSize"]
        # pageSize.setPlaceholderText("Type page size")

        # page: QLineEdit = parameters["page"]
        # page.setPlaceholderText("Type page number")