using OllamaSharp;
using ai_news_aggregator_and_summarizer.Models;
using OllamaSharp.Models;

namespace ai_news_aggregator_and_summarizer.Services;

public static class SummaryService
{
    private static string summaryText = "";
    private static readonly OllamaApiClient ollama = OllamaService.Ollama;
    private static string selectedModel = "";
    private const string messagePrompt = """
        Analyze this news article and summarize it. 
        Only include the summarization. 
        Do not include anything unrelated such as \"Here's a summary of the article:\". 
        Only return the summary of the news article and nothing more.
        The summary must be 1000 characters or less.
        """;

    // Contacts local ollama model and Initializes summaryText;
    private static async Task Summarize(string articleText)
    {
        await foreach (var stream in ollama.GenerateAsync($"{messagePrompt}\n{articleText}"))
        {
            summaryText += stream?.Response;
        }
    }

    // Returns a new Summary object.
    public static async Task<Summary> GetSummary(string articleText)
    {
        if (selectedModel == "")
        {
            return new Summary("The Ollama model is not configured properly.");
        }

        summaryText = "";
        await Summarize(articleText);
        return new Summary(summaryText);
    }

    // Make static localModels variable and only run this method to refresh local models available?
    public static List<string> ListLocalModels()
    {
        List<string> localModels = new List<string>();
        foreach (Model localModel in ollama.ListLocalModelsAsync().Result)
        {
            localModels.Add(localModel.Name);
        }

        return localModels;
    }

    // Checks to see if the model is actually downloaded and valid.
    public static bool IsModelValid(string model)
    {
        List<string> localModels = ListLocalModels();
        return localModels.Contains(model);
    }

    public static string SelectedModel
    {
        get 
        { 
            return selectedModel;
        }
        set 
        { 
            ollama.SelectedModel = value; 
            selectedModel = value;
        }
    }
}
