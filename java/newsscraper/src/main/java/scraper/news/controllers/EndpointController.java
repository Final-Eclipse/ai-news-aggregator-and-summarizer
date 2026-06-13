package scraper.news.controllers;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import scraper.news.services.CreateEndpointService;
import scraper.news.services.newsapi_endpoints.EverythingEndpoint;
import scraper.news.services.newsapi_endpoints.TopHeadlinesEndpoint;
import scraper.news.services.newsapi_endpoints.SourcesEndpoint;
import scraper.news.services.NewsScraper;
import scraper.news.services.EndpointService;
import scraper.news.models.data_transfer_objects.ArticleTextDto;
import scraper.news.models.data_transfer_objects.EndpointDto;

@RestController
public class EndpointController 
{
    private String apiEndpointUrl;

    @PostMapping("/api/v1/news/post-endpoint-data")
    public ResponseEntity<String> postEndpointData(@RequestBody EndpointDto endpointData)
    { 
        EndpointService endpoint = CreateEndpointService.create(endpointData);
        apiEndpointUrl = endpoint.getApiEndpointUrl();
        System.out.println(apiEndpointUrl);
        return ResponseEntity.ok("Successful post! Make summary call to C# and return here eventually. " + apiEndpointUrl);
    }

    @GetMapping("/api/v1/news/everything")
    public String everything()
    {
        EverythingEndpoint x = new EverythingEndpoint.Builder()
            // Use URL encoding to add "%20" between spaces (ex. department of justice -> department%20of%20justice).
            // Wrap q in double quotes for exact phrase.
            // Can also use URL encoding to add double quotes (ex. united states -> %22united%20states%22).
            .q("trump")    // Add another boolean parameter, exactPhrase. Or detect if the user types double quotes and convert that if needed (ex. "\"south korea\"")
            .searchIn("title")
            .sources("associated-press")
            .domains("apnews.com, nbcnews.com")
            .excludeDomains("foxnews.com")
            .from("2026-05-10")
            .to("2026-05-15")
            .language("en")
            .sortBy(null)
            .pageSize("10")
            .page("1")
            .build();

        return NewsScraper.getResponse(x.getApiEndpointUrl());
    }

    @GetMapping("/api/v1/news/top-headlines")
    public String topHeadlines()
    {
        TopHeadlinesEndpoint y = new TopHeadlinesEndpoint.Builder()
            .country("US")
            .category("general")
            // .sources("associated-press") // Can't mix the sources parameter with the country or category parameters.
            .q("trump")
            .pageSize("10")
            .page("1")
            .build();

        return NewsScraper.getResponse(y.getApiEndpointUrl());
    }

    @GetMapping("/api/v1/news/top-headlines/sources")
    public String sources()
    {
        SourcesEndpoint z = new SourcesEndpoint.Builder()
            .category("sports")
            .language("en")
            .country("us")
            .build();

        return NewsScraper.getResponse(z.getApiEndpointUrl());
    }

    @PostMapping("/api/v1/news/summary")
    public ResponseEntity<String> summarization(@RequestBody ArticleTextDto articleText)
    {     
        String text = articleText.getArticleText();
        String summary = NewsScraper.getSummarization(text);
        return ResponseEntity.ok(summary);
    }
}
