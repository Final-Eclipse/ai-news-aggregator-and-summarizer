from PyQt5.QtWidgets import QComboBox, QGridLayout, QWidget
from endpoint import Endpoint

class Sources(Endpoint):
    def __init__(self) -> None:
        self.parameters: dict = self.init_parameters()

        self.layout: QGridLayout = self._create_layout()
        self.container: QWidget = self._create_container(self.layout)

        self._init_fields()
        self.hide()
    
    def init_parameters(self) -> dict:
        parameters = {
            "category": QComboBox(),
            "language": QComboBox(),
            "country": QComboBox()
        }

        return parameters
    
    def _init_fields(self) -> None:
        parameters = self.parameters
    
        category: QComboBox = parameters["category"]
        category.addItems(["Select category", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])
        
        language: QComboBox = parameters["language"]
        language.addItems(["Select language", "English", "Spanish", "German"])

        country: QComboBox = parameters["country"]
        country.addItems(["Select country", "United States", "Canada", "Mexico"])