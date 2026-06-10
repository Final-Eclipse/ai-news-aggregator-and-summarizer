package scraper.news.controllers;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import scraper.news.CreateEndpoint;
import scraper.news.Endpoint;
import scraper.news.EverythingEndpoint;
import scraper.news.NewsScraper;
import scraper.news.SourcesEndpoint;
import scraper.news.TopHeadlinesEndpoint;
import scraper.news.dtos.ArticleTextDto;
import scraper.news.dtos.EndpointDto;

@RestController
public class EndpointController 
{
    // private final ObjectMapper objectMapper = new ObjectMapper();
    private String apiEndpointUrl;

    @PostMapping("/api/v1/news/post-endpoint-data")
    public ResponseEntity<String> postEndpointData(@RequestBody EndpointDto endpointData)
    // public String postEndpointData(@RequestBody String endpointData)
    { 
        // HashMap<String, String> endpointDataHashMap = objectMapper.readValue(endpointData, new TypeReference<>() {});
        // apiEndpointUrl = CreateEndpoint.create(endpointDataHashMap).getApiEndpointUrl();
        // System.out.println(apiEndpointUrl);
        // return "Successful post! Make summary call to C# and return here eventually. " + apiEndpointUrl;

        // Use data transfer object?
        // https://www.appsdeveloperblog.com/read-json-request-body-in-spring-web-mvc/
        // endpointData.initalizeEndpoint();
        // System.out.println(endpointData.getApiEndpointUrl());
        // System.out.println(endpointData.getQ());

        Endpoint endpoint = CreateEndpoint.create(endpointData);
        apiEndpointUrl = endpoint.getApiEndpointUrl();
        // System.out.println(endpointData.getSearchIn());
        System.out.println(apiEndpointUrl);

        return ResponseEntity.ok("Success");
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
