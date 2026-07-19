# import get_data

if __name__ == "__main__":
    from http_service import HttpService
    from localhosts import Localhosts
    from ollama_models import OllamaModels
    from worker import Worker
else:
    from .http_service import HttpService
    from .localhosts import Localhosts
    from .ollama_models import OllamaModels
    from .worker import Worker