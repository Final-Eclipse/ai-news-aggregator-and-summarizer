using Microsoft.AspNetCore.Mvc;
using ai_news_aggregator_and_summarizer.Services;
using ai_news_aggregator_and_summarizer.Models;

namespace ai_news_aggregator_and_summarizer.Controllers;

[ApiController]
[Route("[controller]")]
public class SelectedModelController : ControllerBase
{
    // Return model currently selected.
    [HttpGet("current-model")]
    public string GetCurrentModel()
    {
        return SummaryService.SelectedModel;
    }

    // Return IActionResult, ActionResult, or IEnumerable?
    [HttpGet("available-models")]
    public OllamaModelsDto GetLocalModels()
    {
        // Figure out a way to prevent controllers from running if Ollama isn't running.
        return new OllamaModelsDto();
    }

    [HttpPost]
    public string PostSelectedModel([FromBody] string newModel)
    {
        System.Console.WriteLine(newModel);
        // int offset = 3;
        // int start = newModel.IndexOf(": ") + offset;
        // int end = newModel.IndexOf("\"}");

        // newModel = newModel.Substring(0, end);
        // newModel = newModel.Substring(start);

        if (SummaryService.IsModelValid(newModel) == false)
        {
            return $"Invalid Ollama model selected.";
        }

        SummaryService.SelectedModel = newModel;
        return $"Successfully changed Ollama model to {newModel}.";
    }
}