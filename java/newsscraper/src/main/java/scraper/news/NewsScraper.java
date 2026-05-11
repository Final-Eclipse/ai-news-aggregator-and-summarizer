package scraper.news;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.net.URI;

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
