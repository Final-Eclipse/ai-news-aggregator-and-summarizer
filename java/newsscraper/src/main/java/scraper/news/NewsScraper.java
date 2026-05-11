package scraper.news;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.net.URI;

// Newsapi has 100/day request limit or 1000/day.
// Could scrape news sites directly.
// Could get most popular articles from today from newsapi go to the urls it provides and scrape the information from those links. Then save information to a file for documenting.
// Could get all information through api, though most likely not due to rate limits.

// Thenewsapi is an alternative but with harsher limit restrictions.

/*
API Name            Free Tier Limit         Why it's better
NewsData.io         ~200-500 credits/day    Often double or triple the NewsAPI limit. It has great coverage for non-English news as well.
GNews               100 requests/day        Same count as NewsAPI, but their "search" is often more relevant and less likely to return "broken" links.
TheNewsAPI          300 requests/mont       hLow daily limit, but they allow for more "Global" data access than the NewsAPI free tier.
*/

public class NewsScraper 
{
    private String apiEndpointUrl;
    private HttpClient client = HttpClient.newHttpClient();
    private String apiKey = System.getenv("NEWSAPI_API_KEY");

    public NewsScraper(String apiEndpointUrl)
    {
        this.apiEndpointUrl = apiEndpointUrl;
    }
    
    protected void getResponse()
    {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiEndpointUrl))
            .header("x-api-key", apiKey)
            .build();

        client.sendAsync(request, BodyHandlers.ofString())
            .thenApply(HttpResponse::body)
            .thenAccept(System.out::println)
            .join();
    }    
}
