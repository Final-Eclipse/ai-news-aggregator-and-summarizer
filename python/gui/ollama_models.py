import subprocess, asyncio
from asyncio.subprocess import Process

class OllamaModels():
    @staticmethod
    async def fetch_ollama_models() -> dict:
        """Get all downloaded Ollama models and their details."""
        process = await asyncio.create_subprocess_shell(
            cmd="ollama ls",
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

        model_details_list = await OllamaModels.__assemble_model_details_list(process)
        model_info = OllamaModels.__assemble_model_info_dict(model_details_list)

        await process.communicate()
        return model_info

    @staticmethod
    async def __assemble_model_details_list(process: Process) -> list:
        """Assemble and return a list of Ollama models and their details."""
        model_details_list = []   
        line = await process.stdout.readline()  # Skips the first line of the output.

        while True:
            line = await process.stdout.readline()
            line = line.decode().strip()

            if not line:
                break

            for element in line.split("  "):
                if element == "":
                    continue
                
                model_details_list.append(element.strip())
        
        return model_details_list

    @staticmethod
    def __assemble_model_info_dict(model_details_list: list) -> dict:
        """Assemble and return a dictionary of Ollama models and their details."""
        model_info = {}
        for model_number, index in enumerate(range(0, int(len(model_details_list) / 4)), 1):
            offset = index * 4
            model_info[model_number] = {}
            model_info[model_number]["NAME"] = model_details_list[offset]  
            model_info[model_number]["ID"] = model_details_list[offset + 1]
            model_info[model_number]["SIZE"] = model_details_list[offset + 2]
            model_info[model_number]["MODIFIED"] = model_details_list[offset + 3] 
        return model_info
    
if __name__ == "__main__":
    print(asyncio.run(OllamaModels.fetch_ollama_models()))