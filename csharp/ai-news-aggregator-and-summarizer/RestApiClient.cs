namespace ai_news_aggregator_and_summarizer;

public class RestApiClient
{
    private static HttpClient client = new HttpClient();
    
    // Sparkjava
    // private static string[] endpoints = {"EverythingEndpoint", "TopHeadlinesEndpoint", "SourcesEndpoint"};

    // Spring Boot
    private static string[] endpoints = {"api/v1/news/everything", "api/v1/news/top-headlines", "api/v1/news/top-headlines/sources", "api/v1/news/summary"};

    public static void PrintResponse()
    {
        foreach (string endpoint in endpoints)
        {
            string response = GetResponse(endpoint)
                .GetAwaiter()
                .GetResult();

            System.Console.WriteLine(response);
            System.Console.WriteLine();
            System.Console.WriteLine();
        }
    }

    protected static async Task<string> GetResponse(string endpoint)
    {
        // Sparkjava
        // var response = await client.GetAsync($"http://localhost:4567/{endpoint}"); 

        // Spring Boot
        var response = await client.GetAsync($"http://localhost:8080/{endpoint}");

        var responseBody = await response.Content.ReadAsStringAsync();
        
        if (response.IsSuccessStatusCode == false)
        {
            throw new Exception($"Error Code {response.StatusCode}");
        }

        return responseBody;
    }

    public static async Task PostSummarization(string endpoint, HttpContent summarization)
    {
        // Sparkjava
        // var response = await client.PostAsync($"http://localhost:4567/{endpoint}", summarization);
        
        // Spring Boot
        var response = await client.PostAsync($"http://localhost:8080/{endpoint}", summarization);
    }
}
