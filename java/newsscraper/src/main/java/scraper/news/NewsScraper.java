package scraper.news;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.net.URI;

public class NewsScraper 
{
    private HttpClient client = HttpClient.newHttpClient();
    private String apiKey = System.getenv("NEWSAPI_API_KEY");

    protected String getResponse(String apiEndpointUrl)
    {   
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiEndpointUrl))
            .header("x-api-key", apiKey)
            .build();

        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();

        if (response.statusCode() != 200)
        {
            throw new RuntimeException("Error Code " + response.statusCode());
        }

        return response.body();
    }    
}
