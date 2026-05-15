package scraper.news.newscontroller;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import scraper.news.EverythingEndpoint;
import scraper.news.NewsScraper;
import scraper.news.SourcesEndpoint;
import scraper.news.TopHeadlinesEndpoint;

@RestController
public class EndpointController 
{
    private static NewsScraper newsScraper = new NewsScraper();
    private String summary = "Summary failed!";

    @GetMapping("/test")
    public String test()
    {
        return "Successful Test";
    }

    @GetMapping("/springboot")
    public String springBoot()
    {
        return "spring boot";
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
            .from("2026-04-20")
            .to("2026-04-24")
            .language("en")
            .sortBy(null)
            .pageSize("10")
            .page("1")
            .build();

        return newsScraper.getResponse(x.getApiEndpointUrl());
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

        return newsScraper.getResponse(y.getApiEndpointUrl());
    }

    @GetMapping("/api/v1/news/top-headlines/sources")
    public String sources()
    {
        SourcesEndpoint z = new SourcesEndpoint.Builder()
            .category("sports")
            .language("en")
            .country("us")
            .build();

        return newsScraper.getResponse(z.getApiEndpointUrl());
    }

    @PostMapping("/api/v1/news/summary")
    public void summarization(@RequestParam(value = "summary", defaultValue = "Summary failed!") String summary)    // @RequestParam is a query parameter. Try using @RequestBody instead.
    {
        System.out.println("posting summary");
        this.summary = summary;
    }

    @GetMapping("/api/v1/news/summary")
    public String summarization()
    {
        System.out.println("getting summary");
        System.out.println("The summary is " + summary);
        return summary;
    }
}
