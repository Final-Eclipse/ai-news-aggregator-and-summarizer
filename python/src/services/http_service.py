import requests, asyncio, aiohttp

class HttpService():
    # @staticmethod
    # async def get_local_ollama_models() -> dict:
    #     """Return a new OllamaModelsDto that contains all local Ollama models installed."""
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get("http://localhost:8080/api/v1/models/ollama") as response:
    #             local_models: dict = await response.json()
        
    #     return local_models

    # @staticmethod
    # def main():
    #     loop = asyncio.get_event_loop()
    #     local_models = loop.run_until_complete(HttpService.get_local_ollama_models())
    #     print(local_models)
    #     return local_models
    
    # Move to worker.py
    @staticmethod
    def get_local_ollama_models() -> dict:
        return requests.get("http://localhost:8080/api/v1/models/ollama").json()
