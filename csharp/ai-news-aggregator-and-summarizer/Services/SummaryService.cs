using OllamaSharp;
using ai_news_aggregator_and_summarizer.Models;

namespace ai_news_aggregator_and_summarizer.Services;

public static class SummaryService
{
    public static string? summaryText;
    public static readonly Uri uri = new Uri("http://localhost:11434");
    public static readonly OllamaApiClient ollama = new OllamaApiClient(uri);
    private const string messagePrompt = """
        Analyze this news article and summarize it. 
        Only include the summarization. 
        Do not include anything unrelated such as \"Here's a summary of the article:\". 
        Only return the summary of the news article and nothing more
        """;

    // public static string selectedModel = "";

    static SummaryService()
    {   
        // Throws AggregateException and HttpRequestException if selected model does not exist on the user's computer.
        ollama.SelectedModel = "llama3.1:8b";  // Have selected model as query parameter?
        // ollama.SelectedModel = "huihui_ai/deepseek-r1-abliterated:8b";
        // ollama.SelectedModel = selectedModel;
        // System.Console.WriteLine(ollama.SelectedModel);
    }

    // Contacts local ollama model and Initializes summaryText;
    public static async Task Summarize(string articleText)
    {
        // await foreach (var stream in ollama.GenerateAsync($"Can you summarize this article? {articleText}"))
        await foreach (var stream in ollama.GenerateAsync($"{messagePrompt}\n{articleText}"))
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
