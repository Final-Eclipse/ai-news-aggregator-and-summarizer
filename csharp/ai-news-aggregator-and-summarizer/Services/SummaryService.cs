using OllamaSharp;
using ai_news_aggregator_and_summarizer.Models;

namespace ai_news_aggregator_and_summarizer.Services;

public static class SummaryService
{
    static string? summaryText;
    static readonly Uri uri = new Uri("http://localhost:11434");
    static readonly OllamaApiClient ollama = new OllamaApiClient(uri);

    static SummaryService()
    {    
        // Throws AggregateException and HttpRequestException if selected model does not exist on the user's computer.
        ollama.SelectedModel = "huihui_ai/deepseek-r1-abliterated:8b";  // Have selected model as query parameter?
    }

    // Contacts local ollama model and Initializes summaryText;
    public static async Task Summarize(string articleText)
    {
        await foreach (var stream in ollama.GenerateAsync(articleText))
        {
            summaryText += stream?.Response;
        }
    }

    // Returns a new Summary object.
    public static async Task<Summary> Get(string articleText)
    {
        summaryText = "";
        await Summarize(articleText);
        return new Summary(summaryText);
    }
}
