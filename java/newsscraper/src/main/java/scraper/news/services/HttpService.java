package scraper.news.services;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.IOException;
import java.net.URI;

import tools.jackson.databind.ObjectMapper;

import scraper.news.models.data_transfer_objects.EverythingDto;
import scraper.news.models.data_transfer_objects.OllamaModelsDto;
import scraper.news.models.data_transfer_objects.SourcesDto;
import scraper.news.models.data_transfer_objects.TopHeadlinesDto;

import java.io.File;
import java.util.Scanner;

public class HttpService 
{
    private final static HttpClient client = HttpClient.newHttpClient();
    private static String apiKey;
    private final static ObjectMapper objectMapper = new ObjectMapper();

    /**
     * Sets the API key to the parameter's value.
     * 
     * @param newApiKey
     * @return
     */
    public static String setApiKey(String newApiKey)
    {
        apiKey = newApiKey;
        return "Successfully changed API key.";
    }

    /**
     * Gets the API key from the .env file.
     * 
     * @return API key.
     * @throws IOException
     */
    public static String getApiKey() throws IOException
    {
        Path filePath = Paths.get(Paths.get("").toAbsolutePath().getParent().getParent().toString() + "/python/src/.env");
        File file = new File(filePath.toString());
        String apiKey;

        try (Scanner scanner = new Scanner(file))
        {
            apiKey = scanner.nextLine();
            apiKey = apiKey.substring(apiKey.indexOf("=") + 2, apiKey.length() - 1);
        }

        return apiKey;
    }

    /**
     * Makes an HTTP GET request to NewsAPI and returns the result as a String.
     * 
     * @param apiEndpointUrl String URL pointing to one of NewsAPI's endpoints.
     * @return String representation of the JSON result.
     */
    private static String getNewsApiResponse(String apiEndpointUrl)
    {   
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiEndpointUrl))
            .header("x-api-key", apiKey)
            .GET()
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

    public static String getWebsiteResponse(String url)
    {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(url))
            .build();

        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();
        handleErrorCodes(response);
        return response.body();
    }

    // Have post articleText and getSummarization as different methods?
    /**
     * Makes a HTTP POST request to localhost:5172 (ASP.NET Core) and returns a summary of the given article.
     * 
     * @param articleText String of an article's content.
     * @return String summarization of the article.
     */
    public static String getSummarization(String articleText)
    {
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

    public static String getCurrentOllamaModel()
    {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("http://localhost:5172/selectedmodel/current-model"))
            .header("Content-Type", "application/json")
            .GET()
            .build();
        
        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();

        handleErrorCodes(response);
        return response.body();
    }

    public static OllamaModelsDto getLocalOllamaModels()
    {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("http://localhost:5172/selectedmodel/available-models"))
            .header("Content-Type", "application/json")
            .GET()
            .build();
        
        HttpResponse<String> response = client.sendAsync(request, BodyHandlers.ofString()).join();
        handleErrorCodes(response);

        OllamaModelsDto ollamaModelsDto = objectMapper.readValue(response.body(), OllamaModelsDto.class);
        return ollamaModelsDto;
    }

    public static String changeOllamaModel(String newModel)
    {
        String jsonString = objectMapper.writeValueAsString(newModel);

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("http://localhost:5172/selectedmodel"))
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
            throw new RuntimeException("[HttpService.handleErrorCodes(HttpResponse<String> response)] Error Code " + response.statusCode());
        }
    }
}
