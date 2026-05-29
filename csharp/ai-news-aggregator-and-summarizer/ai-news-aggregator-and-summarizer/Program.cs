namespace ai_news_aggregator_and_summarizer;

using OllamaSharp;
// https://github.com/awaescher/OllamaSharp/tree/main
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;

public class Program
{   
    public static async Task Main(string[] args)
    {
        // GlobalHttpClient httpClient = new GlobalHttpClient();
        
        // RestApiClient restApiClient = new RestApiClient(GlobalHttpClient.httpClient);
        // restApiClient.PrintResponse();

//         LocalModelClient localModelClient = new LocalModelClient(GlobalHttpClient.httpClient);
//         await localModelClient.SendMessage($"Can you summarize this article. \n{articleText}");
//         Console.Write(localModelClient.GetResponse());


        var builder = WebApplication.CreateBuilder(args);
        builder.Services.AddControllers();

        var app = builder.Build();
        app.UseHttpsRedirection();
        app.UseAuthorization();
        app.MapControllers();
        app.Run();

        // Create new csproj for asp net core.
        // Or have two csprojs in the csharp folder.
    }
}
