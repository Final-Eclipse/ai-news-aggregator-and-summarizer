from PyQt5.QtWidgets import QComboBox, QGridLayout, QWidget
from endpoints.endpoint import Endpoint
from endpoints.helpers import Language, Category, Country
import json

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
        category.addItems(Category.qcombobox_options)
        
        language: QComboBox = parameters["language"]
        language.addItems(Language.qcombobox_options)

        country: QComboBox = parameters["country"]
        country.addItems(Country.qcombobox_options)

    def get_database_bindings(self, endpoint_type) -> dict:
        """Return a dictionary of values to use as bindings for database querying."""
        json_str = self.get_json(endpoint_type)
        query: dict = json.loads(json_str)

        # Remove unnecessary keys.
        query.pop("endpoint")

        # Format values.
        for key, value in query.items():
            if key == "from" or key == "to":
                if value is None:
                    query[key] = ""
                continue

            if value is None:
                value = ""

            query[key] = f"%{value}%"
        
        return query