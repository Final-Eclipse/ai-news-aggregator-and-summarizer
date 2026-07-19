import sys, pathlib
sys.path.append(f"{pathlib.Path.cwd()}")

from PyQt5.QtWidgets import QComboBox, QLineEdit, QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt
import json
from src.gui.helpers import Language, Country

class Endpoint():
    def __init__(self):
        self.parameters: dict
        self.layout: QGridLayout 
        self.container: QWidget

    def _convert_language_to_iso_code(self, language) -> str:
        if language in Language.codes: 
            return Language.codes[language] 
        else:
            return None
        
    def _convert_country_to_iso_code(self, country) -> str:
        if country in Country.codes:
            return Country.codes[country]
        else:
            return None

    def _get_widget_text(self, widget) -> str:
        text: str = ""

        if type(widget) == QComboBox:
            if widget.currentIndex() != 0:
                text = widget.currentText()

        elif type(widget) == QLineEdit:
            text = widget.text()

        return text

    def get_json(self, endpoint_type) -> str:
        json_dict = {}
        json_dict["endpoint"] = endpoint_type

        for key, widget in self.parameters.items():
            text = self._get_widget_text(widget)

            language_code = self._convert_language_to_iso_code(text)
            if language_code != None:
                text = language_code
            
            country_code = self._convert_country_to_iso_code(text)
            if country_code != None:
                text = country_code

            if text == "":
                text = None

            if text != None:
                text = text.replace(" ", "-")

            json_dict[key] = text

        return json.dumps(json_dict)

    def _create_layout(self) -> QGridLayout: 
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.setHorizontalSpacing(10)
        
        row = 0
        col = 0
        for key, widget in self.parameters.items():
            label = QLabel(key)
            label.setAlignment(Qt.AlignmentFlag.AlignBottom)
            
            layout.addWidget(label, row, col)
            layout.addWidget(widget, row + 1, col)

            col += 1

        return layout

    def _create_container(self, layout) -> QWidget:
        container = QWidget()
        container.setLayout(layout)
        
        # font = container.font()
        # font.setPointSize(16)
        # container.setFont(font)
        
        return container
    
    def _init_widget_sizes(self) -> None:
        for key, widget in self.parameters.items():
            widget: QWidget
            max_width = widget.sizeHint().width()
            widget.setMaximumWidth(max_width)

    def hide(self) -> None:
        self.container.hide()

    def show(self) -> None:
        self.container.show()