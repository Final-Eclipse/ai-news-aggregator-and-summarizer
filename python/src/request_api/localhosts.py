import asyncio
from pathlib import Path

class Localhosts():
    @staticmethod
    async def _run_dotnet() -> None:
        """Start the ASP.NET Core dotnet localhost."""
        process = await asyncio.create_subprocess_shell(
            cmd="dotnet run",
            cwd=f"{Path.cwd().parent}/csharp/ai-news-aggregator-and-summarizer"
        )

        await process.communicate()
    
    @staticmethod
    async def _run_java() -> None:
        """Start the Java Spring Boot localhost."""
        process = await asyncio.create_subprocess_shell(
            cmd="mvnw.cmd spring-boot:run",
            cwd=f"{Path.cwd().parent}/java/newsscraper"
        )

        await process.communicate()

    @staticmethod
    async def _run_ollama() -> None:
        """Start the Ollama localhost."""
        process = await asyncio.create_subprocess_shell(
            cmd="ollama serve"
        )

        await process.communicate()

    @staticmethod
    async def run_localhosts() -> None:
        """Call and start all localhosts."""
        tasks = [
            Localhosts._run_dotnet(), 
            Localhosts._run_java(), 
            Localhosts._run_ollama()
        ]
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(Localhosts.run_localhosts())