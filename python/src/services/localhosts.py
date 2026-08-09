import asyncio
from pathlib import Path
from PyQt5.QtCore import QRunnable, pyqtSlot
import subprocess

class Localhosts(QRunnable):
    def __init__(self):
        super().__init__()

        self.processes = []

    @pyqtSlot()
    def run(self) -> None:
        self._run_java()
        self._run_dotnet()
        self._run_ollama()

    def _run_java(self) -> None:
        process = subprocess.Popen(["mvnw.cmd", "spring-boot:run"], text=True, cwd=f"{Path.cwd().parent}/java/newsscraper", shell=True)
        self.processes.append(process)

    def _run_dotnet(self) -> None:
        process = subprocess.Popen(["dotnet", "run"], text=True, cwd=f"{Path.cwd().parent}/csharp/ai-news-aggregator-and-summarizer", shell=True)
        self.processes.append(process)

    def _run_ollama(self) -> None:
        process = subprocess.Popen(["ollama", "serve"], text=True, shell=True)
        self.processes.append(process)

    def stop(self) -> None:
        for process in self.processes:
            process: subprocess.Popen
            process.kill() 
            print("Process terminated.")

if __name__ == "__main__":
    x = Localhosts()
    x.run()