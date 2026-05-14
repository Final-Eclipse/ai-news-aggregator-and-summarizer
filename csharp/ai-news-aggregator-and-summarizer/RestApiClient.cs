namespace ai_news_aggregator_and_summarizer;

public class RestApiClient
{
    private static HttpClient client = new HttpClient();
    private static string[] endpoints = {"EverythingEndpoint", "TopHeadlinesEndpoint", "SourcesEndpoint"};

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
        var response = await client.GetAsync($"http://localhost:4567/{endpoint}");
        var responseBody = await response.Content.ReadAsStringAsync();
        
        if (response.IsSuccessStatusCode == false)
        {
            throw new Exception($"Error Code {response.StatusCode}");
        }

        return responseBody;
    }

    public static async Task PostSummarization(string endpoint, HttpContent summarization)
    {
        var response = await client.PostAsync($"http://localhost:4567/{endpoint}", summarization);
    }
}
