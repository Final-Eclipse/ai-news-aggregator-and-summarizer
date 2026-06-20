using OllamaSharp;

namespace ai_news_aggregator_and_summarizer.Services;

public static class OllamaService
{
    private static readonly Uri ollamaLocalHost = new Uri("http://localhost:11434");
    private static readonly OllamaApiClient ollama = new OllamaApiClient(ollamaLocalHost);
    
    public static bool IsOllamaRunning()
    {
        return ollama.IsRunningAsync().Result;
    }

    public static string GetOllamaNotRunningErrorMessage()
    {
        return "Ollama is not currently running.";
    }

    public static OllamaApiClient Ollama
    {
        get { return ollama; }
    }
}