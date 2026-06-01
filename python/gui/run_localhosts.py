import subprocess, keyboard, os
from pathlib import Path

def run_dotnet():
    x = subprocess.Popen(
        ["dotnet", "run"],
        stdout=subprocess.PIPE,
        text=True,
        cwd=f"{Path.cwd().parent}/csharp/ai-news-aggregator-and-summarizer",
        shell=True
    )

    # print(x.stdout)
    # print(x.stderr)
    # print(x.returncode)

def run_java():
    x = subprocess.Popen(
            ["mvnw.cmd", "spring-boot:run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(f"{Path.cwd().parent}/java/newsscraper"),
            shell=True
    )

    # print(x.stdout)
    # print(x.stderr)
    # print(x.returncode)

def terminate_program():
    while keyboard.is_pressed("esc") == False:
        pass

    raise Exception("Escape pressed, terminating programs.")


run_dotnet()
run_java()
terminate_program()

