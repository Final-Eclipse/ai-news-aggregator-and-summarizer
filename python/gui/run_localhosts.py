import subprocess
from pathlib import Path

def run_dotnet():
    x = subprocess.Popen(
        ["dotnet", "run"],
        stdout=subprocess.PIPE,
        text=True,
        cwd=f"{Path.cwd().parent}/csharp/ai-news-aggregator-and-summarizer",
        shell=True
    )

def run_java():
    x = subprocess.Popen(
        ["mvnw.cmd", "spring-boot:run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(f"{Path.cwd().parent}/java/newsscraper"),
        shell=True
    )

def run_ollama():
    x = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        text=True,
        shell=True
    )

def main():
    run_dotnet()
    run_java()
    run_ollama()

if __name__ == "__main__":
    main()