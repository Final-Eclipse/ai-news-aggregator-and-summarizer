namespace ai_news_aggregator_and_summarizer;

// Only one instance should ever be created!
// This instance should be shared across all clients.
public class GlobalHttpClient
{
    public static HttpClient httpClient = new HttpClient();
}