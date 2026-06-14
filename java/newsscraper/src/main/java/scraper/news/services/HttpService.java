package scraper.news.services;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.net.URI;

import tools.jackson.databind.ObjectMapper;

import scraper.news.models.data_transfer_objects.EverythingDto;
import scraper.news.models.data_transfer_objects.SourcesDto;
import scraper.news.models.data_transfer_objects.TopHeadlinesDto;

public class HttpService 
{
    private final static HttpClient client = HttpClient.newHttpClient();
    private static String apiKey = System.getenv("NEWSAPI_API_KEY");
    private final static ObjectMapper objectMapper = new ObjectMapper();

    /**
     * Makes an HTTP GET request to NewsAPI and returns the result as a String.
     * 
     * @param apiEndpointUrl String URL pointing to one of NewsAPI's endpoints.
     * @return String representation of the JSON result.
     */
    public static String getNewsApiResponse(String apiEndpointUrl)
    {   
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiEndpointUrl))
            .header("x-api-key", apiKey)
            .build();

        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();
        handleErrorCodes(response);
        return response.body();
    }    

    public static EverythingDto getEverythingResponse(String apiEndpointUrl)
    {
        String responseBody = getNewsApiResponse(apiEndpointUrl);
        EverythingDto everythingResponse = objectMapper.readValue(responseBody, EverythingDto.class);
        return everythingResponse;
    }

    public static TopHeadlinesDto getTopHeadlinesResponse(String apiEndpointUrl)
    {
        String responseBody = getNewsApiResponse(apiEndpointUrl);
        TopHeadlinesDto topHeadlinesResponse = objectMapper.readValue(responseBody, TopHeadlinesDto.class);
        return topHeadlinesResponse;
    }

    public static SourcesDto getSourcesResponse(String apiEndpointUrl)
    {
        String responseBody = getNewsApiResponse(apiEndpointUrl);
        SourcesDto sourcesResponse = objectMapper.readValue(responseBody, SourcesDto.class);
        return sourcesResponse;
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
