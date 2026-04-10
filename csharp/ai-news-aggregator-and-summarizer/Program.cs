using System.Net.Http;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using System;

// Do the news websites have apis.

// using var client = new HttpClient();
// var response = await client.GetAsync("https://myanimelist.net");
// var content = await response.Content.ReadAsStringAsync();
// System.Console.WriteLine(content);

class Scraper
{   
//     string apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY")!;
    
    private static HttpClient client = new HttpClient();

    public static void Main(string[] args)
    {
        // SetBaseAddress();
        // GetResponse().GetAwaiter().GetResult();
        System.Console.WriteLine("test");
    }

    private static void SetBaseAddress()
    {
        client.BaseAddress = new Uri("https://api.ap.org");
    }

    static async Task GetResponse()
    {
        // client.DefaultRequestHeaders.Add("x-api-key", "");
        var response = await client.GetAsync("https://myanimelist.net");

        var responseBody = await response.Content.ReadAsStringAsync();
        System.Console.WriteLine(response.IsSuccessStatusCode);
        System.Console.WriteLine(responseBody);
    }
}
