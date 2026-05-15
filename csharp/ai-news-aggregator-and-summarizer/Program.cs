namespace ai_news_aggregator_and_summarizer;

public class Program
{   
    public static async Task Main(string[] args)
    {
        // RestApiClient.PrintResponse();
        
        // Start localhost then run this.
        // Refresh localhost to show posted data.
        HttpContent httpContent = new StringContent("testing if this will post", System.Text.Encoding.UTF8, "text/plain");
        await RestApiClient.PostSummarization("api/v1/news/summary", httpContent);  // This doesn't work
        await RestApiClient.PostSummarization("api/v1/news/summary?summary=posting_summary", httpContent);  // This does work because @RequestParam is a query parameter.
    }
}
