package scraper.news;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;

import tools.jackson.databind.ObjectMapper;

import java.net.URI;

public class NewsScraper 
{
    private static HttpClient client = HttpClient.newHttpClient();
    private static String apiKey = System.getenv("NEWSAPI_API_KEY");

    public static String getResponse(String apiEndpointUrl)
    {   
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiEndpointUrl))
            .header("x-api-key", apiKey)
            .build();

        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();
        handleErrorCodes(response);

        return response.body();
    }    

    public static String getSummarization(String articleText)
    {
        // Serializes articleText as a JSON String.
        ObjectMapper objectMapper = new ObjectMapper();
        String jsonString = objectMapper.writeValueAsString(articleText);

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("http://localhost:5172/summary"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonString))
            .build();
        
        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();
        handleErrorCodes(response);
        
        return response.body();
    }

    private static void handleErrorCodes(HttpResponse<String> response)
    {
        if (response.statusCode() != 200)
        {
            throw new RuntimeException("Error Code " + response.statusCode());
        }
    }
}
