namespace ai_news_aggregator_and_summarizer;

public class RestApiClient
{
    private readonly HttpClient httpClient;
    private static string[] endpoints = {"api/v1/news/everything", "api/v1/news/top-headlines", "api/v1/news/top-headlines/sources", "api/v1/news/summary"};

    public RestApiClient(HttpClient x)
    {
        httpClient = x;
    }
    
    public void PrintResponse()
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

    protected async Task<string> GetResponse(string endpoint)
    {
        var response = await httpClient.GetAsync($"http://localhost:8080/{endpoint}");
        var responseBody = await response.Content.ReadAsStringAsync();
        
        if (response.IsSuccessStatusCode == false)
        {
            throw new Exception($"Error Code {response.StatusCode}");
        }

        return responseBody;
    }

    public async Task PostSummarization(string endpoint, HttpContent summarization)
    {
        var response = await httpClient.PostAsync($"http://localhost:8080/{endpoint}", summarization);
    }
}
