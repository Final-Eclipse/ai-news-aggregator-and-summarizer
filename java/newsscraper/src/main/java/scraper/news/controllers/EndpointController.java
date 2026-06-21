package scraper.news.controllers;

// import java.io.IOException;

// import org.apache.catalina.connector.Response;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import scraper.news.services.CreateEndpointService;
// import scraper.news.services.newsapi_endpoints.EverythingEndpointService;
// import scraper.news.services.newsapi_endpoints.TopHeadlinesEndpointService;
// import scraper.news.services.newsapi_endpoints.SourcesEndpointService;
import scraper.news.services.HttpService;
import scraper.news.services.parsers.Parser;
import scraper.news.services.BaseEndpointService;
// import scraper.news.models.data_transfer_objects.ArticleTextDto;
import scraper.news.models.data_transfer_objects.EndpointDto;
import scraper.news.models.data_transfer_objects.EverythingDto;
import scraper.news.models.data_transfer_objects.OllamaModelsDto;
import scraper.news.models.data_transfer_objects.SourcesDto;
import scraper.news.models.data_transfer_objects.TopHeadlinesDto;

@RestController
public class EndpointController 
{
    private String apiEndpointUrl;
    private EndpointDto endpointData;
    // private Parser parser = new Parser();

    @PostMapping("/api/v1/news/post-endpoint-data")
    public ResponseEntity<String> postEndpointData(@RequestBody EndpointDto endpointData)   // Rename EndpointDto to EndpointDataDto? or something similar.
    { 
        // ✓ Call method to get NewsAPI JSON.
        // X Parse JSON for article urls, article thumbnails, etc.
        // X Scrape each article (either parse the HTML to get the article body or send the entire HTML to C# to summarize the article based off of that).
        this.endpointData = endpointData;
        BaseEndpointService endpoint = CreateEndpointService.create(endpointData);
        apiEndpointUrl = endpoint.getApiEndpointUrl();
        return ResponseEntity.ok("Successful post! Make summary call to C# and return here eventually. " + apiEndpointUrl);
    }

    @GetMapping("/api/v1/news/everything")
    public ResponseEntity<EverythingDto> getEverythingResponse()
    {
        isValidEndpoint("everything");
        return ResponseEntity.ok(HttpService.getEverythingResponse(apiEndpointUrl));
    }

    @GetMapping("/api/v1/news/top-headlines")
    public ResponseEntity<TopHeadlinesDto> getTopHeadlinesResponse()
    {
        isValidEndpoint("top-headlines");
        return ResponseEntity.ok(HttpService.getTopHeadlinesResponse(apiEndpointUrl));
    }

    @GetMapping("/api/v1/news/top-headlines/sources")
    public ResponseEntity<SourcesDto> getSourcesResponse()
    {
        isValidEndpoint("top-headlines/sources");
        return ResponseEntity.ok(HttpService.getSourcesResponse(apiEndpointUrl));
    }

    // Checks to see if the endpoint type matches the method being called.
    private void isValidEndpoint(String endpointType)
    {
        if (endpointData.getEndpoint().equals(endpointType) == false)
        {
            throw new RuntimeException("Invalid endpoint type.");
        }
    }

    private String getWebsiteHtml(String url)
    {
        return HttpService.getWebsiteResponse(url);
    }

    @PostMapping("/api/v1/news/summary")
    public ResponseEntity<String> summarize(@RequestBody String url) 
    {     
        String websiteHtml = getWebsiteHtml(url);
        String pageContent = Parser.parse(url, websiteHtml);
        String summary = HttpService.getSummarization(pageContent);
        return ResponseEntity.ok(summary);
    }

    @GetMapping("/api/v1/models/ollama")
    public ResponseEntity<OllamaModelsDto> getLocalOllamaModels()
    {
        return ResponseEntity.ok(HttpService.getLocalOllamaModels());
    }

    @PostMapping("/api/v1/models/ollama")
    public ResponseEntity<String> changeOllamaModel()
    {
        return ResponseEntity.ok("");
    }

    

    // @PostMapping("/api/v1/news/summary")
    // public ResponseEntity<String> summarization(@RequestBody ArticleTextDto articleText)
    // {     
    //     String text = articleText.getArticleText();
    //     String summary = HttpService.getSummarization(text);
    //     return ResponseEntity.ok(summary);
    // }

    // private ApiResponse getEndpointResponse(EndpointDto endpointData)
    // {

    //     switch (endpointData.getEndpoint())
    //     {
    //         case "everything":
    //             return HttpService.getEverythingResponse(apiEndpointUrl);
    //         case "top-headlines":
    //             return HttpService.getTopHeadlinesResponse(apiEndpointUrl);
    //         case "top-headlines/sources":
    //             return HttpService.getSourcesResponse(apiEndpointUrl);
    //         default:
    //             throw new RuntimeException("Invalid endpoint type.");
    //     }
    //     // String responseString = HttpService.getNewsApiResponse(apiEndpointUrl);
    //     // return responseString;
    // }

    // // Most likely remove these GET methods and replace with methods that take a url.
    // @GetMapping("/api/v1/news/everything")
    // public String everything()
    // {
    //     EverythingEndpointService x = new EverythingEndpointService.Builder()
    //         // Use URL encoding to add "%20" between spaces (ex. department of justice -> department%20of%20justice).
    //         // Wrap q in double quotes for exact phrase.
    //         // Can also use URL encoding to add double quotes (ex. united states -> %22united%20states%22).
    //         .q("trump")    // Add another boolean parameter, exactPhrase. Or detect if the user types double quotes and convert that if needed (ex. "\"south korea\"")
    //         .searchIn("title")
    //         .sources("associated-press")
    //         .domains("apnews.com, nbcnews.com")
    //         .excludeDomains("foxnews.com")
    //         .from("2026-06-10")
    //         .to("2026-06-12")
    //         .language("en")
    //         .sortBy(null)
    //         .pageSize("10")
    //         .page("1")
    //         .build();

    //     return HttpService.getResponse(x.getApiEndpointUrl());
    // }

    // @GetMapping("/api/v1/news/top-headlines")
    // public String topHeadlines()
    // {
    //     TopHeadlinesEndpointService y = new TopHeadlinesEndpointService.Builder()
    //         .country("US")
    //         .category("general")
    //         // .sources("associated-press") // Can't mix the sources parameter with the country or category parameters.
    //         .q("trump")
    //         .pageSize("10")
    //         .page("1")
    //         .build();

    //     return HttpService.getResponse(y.getApiEndpointUrl());
    // }

    // @GetMapping("/api/v1/news/top-headlines/sources")
    // public String sources()
    // {
    //     SourcesEndpointService z = new SourcesEndpointService.Builder()
    //         .category("sports")
    //         .language("en")
    //         .country("us")
    //         .build();

    //     return HttpService.getResponse(z.getApiEndpointUrl());
    // }
}