from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtCore import Qt

class Endpoint():
    def __init__(self):
        self.parameters: dict
        self.layout: QGridLayout 
        self.container: QWidget

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