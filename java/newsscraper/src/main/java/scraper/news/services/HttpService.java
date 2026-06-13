package scraper.news.services;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.HashMap;

import tools.jackson.databind.ObjectMapper;

import java.net.URI;

public class HttpService 
{
    private final static HttpClient client = HttpClient.newHttpClient();
    private static String apiKey = System.getenv("NEWSAPI_API_KEY");

    /**
     * Makes an HTTP GET request to NewsAPI and returns the result as a String.
     * 
     * @param apiEndpointUrl String URL pointing to one of NewsAPI's endpoints.
     * @return String representation of the JSON result.
     */
    public static String getResponse(String apiEndpointUrl)
    {   
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiEndpointUrl))
            .header("x-api-key", apiKey)
            .build();

        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();
        handleErrorCodes(response);

        // Use global objectMapper for this file?
        // Figure out how to return HashMap representation of the JSON result instead of a String.

        // ObjectMapper objectMapper = new ObjectMapper();
        // HashMap<String, Object> jsonHashMap = objectMapper.readValue(response.body(), HashMap.class);
        // System.out.println(jsonHashMap.get("articles"));

        // String jsonString = (String) jsonHashMap.get("articles");
        // String[] articlesArray = objectMapper.readValue(jsonString, String[].class);
        // System.out.println(articlesArray);

        // String[] articlesArray = (String[]) jsonHashMap.get("articles");
        // System.out.println(articlesArray[0]);
        // String jsonString = objectMapper.writeValueAsString(response.body());
        // return jsonString;

        return response.body();
    }    

    /**
     * Makes a HTTP POST request to localhost:5172 (ASP.NET Core) and returns a summary of the given article.
     * 
     * @param articleText String of an article's content.
     * @return String summarization of the article.
     */
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

    /**
     * Handles non-200 error codes from HTTP responses.
     * 
     * @throws RuntimeException if the response's status code is not 200.
     * @param response HttpResponse<String> that is used to determine the HTTP response's status code.
     */
    private static void handleErrorCodes(HttpResponse<String> response)
    {
        if (response.statusCode() != 200)
        {
            throw new RuntimeException("Error Code " + response.statusCode());
        }
    }
}
