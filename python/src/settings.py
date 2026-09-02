from PyQt5.QtWidgets import QApplication, QGridLayout, QHBoxLayout, QMainWindow, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit, QListWidget
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QThreadPool, QRunnable, QObject, pyqtSlot
from PyQt5.QtGui import QPixmap
import requests
from pathlib import Path
from news_card import NewsCard
from enum import Enum

class Settings(QMainWindow):
    back_button_clicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()

        # Create settings object when gui.py init is called.
        # When settings page is opened, get current model and get local models every time.
        # Can be done using a signal.
        # When gui.py emits signal saying change to setting page, get current and local models and update the labels.
        # Or don't update labels every time.
        # Only update when the refresh button is clicked.
        # Or maybe only create settings page when settings button is clicked, localhosts don't finish setting up in time 
        # before settings is created because they are being created asynchronously.

        self.container = self._create_settings_page()
        self.setCentralWidget(self.container)

    def _fetch_local_models(self) -> list:
        threadpool = QThreadPool().globalInstance()
        worker = HttpWorker(EndpointTypes.GET_LOCAL_MODELS.value)
        worker.signals.local_models.connect(lambda local_models: self.models_list.addItems(local_models))
        threadpool.start(worker)

    def _create_top_container(self) -> QWidget:
        top_layout = QGridLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.back_button_clicked.emit())
        font = back_button.font()
        font.setPointSize(12)
        font.setFamily("Sitka")
        back_button.setFont(font)
        back_button.setFixedSize(50, 50)

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title.font()
        font.setPointSize(20)
        font.setBold(True)
        font.setFamily("Sitka")
        title.setFont(font)

        placeholder = QWidget()
        placeholder.setFixedSize(back_button.size())
        placeholder.setStyleSheet("background-color: red")

        top_layout.addWidget(back_button, 0, 0)
        top_layout.addWidget(title, 0, 1)
        top_layout.addWidget(placeholder, 0, 2)

        top_container = QWidget()
        top_container.setStyleSheet("background-color: #c19bff")
        top_container.setLayout(top_layout)
        top_container.setFixedHeight(top_container.sizeHint().height())

        return top_container

    def _create_api_key_widget(self) -> QWidget:
        api_key_label = QLabel("News API Key")
        api_key_label.setStyleSheet("background-color: #fb9b2b")
        api_key_label.setFixedSize(200, 20)
        api_key_label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        api_key_button = QLineEdit()
        api_key_button.setPlaceholderText("Enter your News API key")
        api_key_button.setFixedSize(200, 20)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)
        layout.addWidget(api_key_label)
        layout.addWidget(api_key_button)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background-color: #2b99fb")

        return container

    def _post_new_model(self, new_model: str) -> None:
        threadpool = QThreadPool().globalInstance()
        worker = HttpWorker(EndpointTypes.POST_NEW_MODEL.value, new_model=new_model)
        worker.signals.new_model.connect(lambda: self._update_current_model_widget(new_model))
        threadpool.start(worker)

    def _create_local_models_widget(self) -> QWidget:
        header = QLabel("Ollama Models")
        header.setFixedSize(header.sizeHint())
        header.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        self.models_list = QListWidget()
        self.models_list.clicked.connect(lambda: self._post_new_model(self.models_list.currentItem().text()))
        self.models_list.setFixedSize(self.models_list.sizeHint())
        self._fetch_local_models()

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self._fetch_local_models)
        refresh_button.setStyleSheet("background-color: #ffd493")
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(header)
        layout.addWidget(self.models_list)
        layout.addWidget(refresh_button)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background-color: #2bfb3c")

        return container

    def _update_current_model_widget(self, new_model) -> None:
        self.current_model_widget.setText(new_model)

    def _create_current_model_widget(self) -> QWidget:
        header = QLabel("Current Model")
        header.setFixedSize(200, 20)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("background-color: #c1ffbe")

        # Fetch current model.
        threadpool = QThreadPool().globalInstance()
        worker = HttpWorker(EndpointTypes.GET_CURRENT_MODEL.value)
        worker.signals.current_model.connect(lambda current_model: self.current_model_widget.setText(current_model))
        threadpool.start(worker)

        self.current_model_widget = QLabel()
        self.current_model_widget.setFixedSize(200, 20)
        self.current_model_widget.setStyleSheet("background-color: #ff5b81")

        layout = QVBoxLayout()
        layout.addWidget(header)
        layout.addWidget(self.current_model_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background-color: #67b7ff")

        return container

    def _create_settings_page(self) -> QWidget:
        top_container = self._create_top_container()
        api_key_widget = self._create_api_key_widget()
        local_models_widget = self._create_local_models_widget()
        current_model_widget = self._create_current_model_widget()

        settings_layout = QHBoxLayout()
        settings_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        settings_layout.addWidget(api_key_widget)
        settings_layout.addSpacing(50)
        settings_layout.addWidget(local_models_widget)

        settings_container = QWidget()
        settings_container.setFixedHeight(500)
        settings_container.setStyleSheet("background-color: yellow")
        settings_container.setLayout(settings_layout)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(top_container)
        main_layout.addWidget(settings_container)
        main_layout.addWidget(current_model_widget)

        main_container = QWidget()
        main_container.setStyleSheet("background-color: pink")
        main_container.setLayout(main_layout)        

        return main_container

class EndpointTypes(Enum):
    GET_CURRENT_MODEL = "current"
    GET_LOCAL_MODELS = "local"
    POST_NEW_MODEL = "change"

class HttpWorker(QRunnable):
    def __init__(self, endpoint_type: str, new_model: None|str=None):
        super().__init__()

        self.endpoint_type = endpoint_type
        self.new_model = new_model
        self.signals = HttpSignals()

    @pyqtSlot()
    def run(self):
        try:
            if self.endpoint_type == EndpointTypes.GET_LOCAL_MODELS.value:
                request = requests.get("http://localhost:8080/api/v1/models/ollama/local-models").json()
                local_models: list
                for key, model in request.items():
                    local_models = model

                self.signals.local_models.emit(local_models)

            elif self.endpoint_type == EndpointTypes.GET_CURRENT_MODEL.value:
                request = requests.get("http://localhost:8080/api/v1/models/ollama/current").text
                if request == "":
                    request = "None"

                self.signals.current_model.emit(request)

            elif self.endpoint_type == EndpointTypes.POST_NEW_MODEL.value:
                request = requests.post("http://localhost:8080/api/v1/models/ollama/change", data=self.new_model).text
                self.signals.new_model.emit(request)

        except requests.exceptions.ConnectionError as e:
            if self.endpoint_type == EndpointTypes.GET_LOCAL_MODELS.value:
                self.signals.local_models.emit([])

            elif self.endpoint_type == EndpointTypes.GET_CURRENT_MODEL.value:
                self.signals.current_model.emit("None")

            elif self.endpoint_type == EndpointTypes.POST_NEW_MODEL.value:
                self.signals.new_model.emit([])
        
class HttpSignals(QObject):
    local_models = pyqtSignal(list)
    current_model = pyqtSignal(str)
    new_model = pyqtSignal(str)

def main() -> None:  
    app = QApplication([])
    window = Settings()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()