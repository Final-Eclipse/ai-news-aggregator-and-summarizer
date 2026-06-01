package scraper.news.newscontroller;

import java.util.HashMap;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import scraper.news.CreateEndpoint;
import scraper.news.EverythingEndpoint;
import scraper.news.NewsScraper;
import scraper.news.SourcesEndpoint;
import scraper.news.TopHeadlinesEndpoint;

import tools.jackson.core.type.TypeReference;
import tools.jackson.databind.ObjectMapper;

@RestController
public class EndpointController 
{
    // private static NewsScraper newsScraper = new NewsScraper();
    private String summary = "Summary failed!";
    private ObjectMapper objectMapper = new ObjectMapper();
    private String apiEndpointUrl;

    @PostMapping("/api/v1/news/post-endpoint-data")
    public String postEndpointData(@RequestBody String endpointData)
    {
        HashMap<String, String> endpointDataHashMap = objectMapper.readValue(endpointData, new TypeReference<>() {});
        apiEndpointUrl = CreateEndpoint.create(endpointDataHashMap).getApiEndpointUrl();
     
        System.out.println(apiEndpointUrl);
        return "Successful post! Make summary call to C# and return here eventually.";
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
    public String summarization(@RequestBody String articleText)    // @RequestParam is a query parameter. Try using @RequestBody instead.
    {
        // System.out.println("posting summary");
        // this.summary = summary;

        // POST article to C# and return the summarization.
        // this.summary variable not needed?
        // Instead create a summary failed placeholder variable?
        // return "successful summarization call";

        HashMap<String, String> articleTextJson = objectMapper.readValue(articleText, new TypeReference<>() {});
        return NewsScraper.getSummarization(articleTextJson.get("articleText"));
        // return NewsScraper.getSummarization(articleText);
        // return "success";
    }

    // Not needed because POST returns a value?
    // @GetMapping("/api/v1/news/summary")
    // public String summarization(@RequestParam String articleText)
    // {
    //     System.out.println("getting summary");
    //     System.out.println("The summary is " + summary);
    //     // return articleText;
    //     return NewsScraper.getSummarization(articleText);
    //     // return summary;
    // }
}
