namespace ai_news_aggregator_and_summarizer;

using System.Text.Json;
using OllamaSharp;

public class LocalModelClient
{
    private HttpClient httpClient;
    private string response = "";

    public LocalModelClient(HttpClient httpClient)
    {
        this.httpClient = httpClient;
    }

    public async Task SendMessage(string message)
    {
        // set up the client
        var uri = new Uri("http://localhost:11434");
        var ollama = new OllamaApiClient(uri);

        // select a model which should be used for further operations
        ollama.SelectedModel = "huihui_ai/deepseek-r1-abliterated:8b";
      
        await foreach (var stream in ollama.GenerateAsync(message))
        {
            response += stream.Response;
        }
    }

    public string GetResponse()
    {
        return response;
    }
}