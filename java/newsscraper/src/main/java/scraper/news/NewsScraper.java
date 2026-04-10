package scraper.news;

import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.net.URI;

// Newsapi has 100/day request limit or 1000/day.
// Could scrape news sites directly.
// Could get most popular articles from today from newsapi go to the urls it provides and scrape the information from those links. Then save information to a file for documenting.
// Could get all information through api, though most likely not due to rate limits.

// Thenewsapi is an alternative but with harsher limit restrictions.

/*
API Name            Free Tier Limit         Why it's better
NewsData.io         ~200-500 credits/day    Often double or triple the NewsAPI limit. It has great coverage for non-English news as well.
GNews               100 requests/day        Same count as NewsAPI, but their "search" is often more relevant and less likely to return "broken" links.
TheNewsAPI          300 requests/mont       hLow daily limit, but they allow for more "Global" data access than the NewsAPI free tier.
*/

public class NewsScraper 
{
    private String apiURL;
    private String country;
    private String category;
    private String sources;
    private String keywords;

    private HttpClient client = HttpClient.newHttpClient();
    // private String apiURL = "https://newsapi.org/v2/top-headlines";
    private String apiKey = System.getenv("NEWSAPI_API_KEY");

    // Constructor.
    // private NewsScraper(Builder builder)
    // {
    //     this.apiURL = builder.apiURL;
    //     this.country = builder.country;
    //     this.category = builder.category;
    // }

    public NewsScraper(String apiURL)
    {
        this.apiURL = apiURL;
    }
    

    // Add & only if a condition passes.
    // If country != null add &.
    // If category == null, the url will be invalid as the url ends with &.
    protected void addQueryParameters()
    {
        apiURL = apiURL + "?";
        if (country != null)
        {
            apiURL = apiURL + "country=" + country + "&";
        }
        if (category != null)
        {
            apiURL = apiURL + "category=" + category + "&";
        }

        // Removes the last &.
        int index = apiURL.lastIndexOf("&");
        apiURL = apiURL.substring(0, index);
    }

    protected void getResponse()
    {
        // String x = new addQueryParameters()
        //     .country = "us"
        //     .category = "politics";
        
        // System.out.println(apiURL);
        // System.out.println(apiKey);
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(apiURL))
            .header("x-api-key", apiKey)
            .build();
        
        // System.out.println(request);

        client.sendAsync(request, BodyHandlers.ofString())
            .thenApply(HttpResponse::body)
            .thenAccept(System.out::println)
            .join();
    }    

    // // Builder.
    // public static class Builder
    // {
    //     private String apiURL;
    //     private String country;
    //     private String category;
    //     private String sources;
    //     private String keywords;

    //     public Builder setApiURL(String apiURL)
    //     {
    //        this.apiURL = apiURL;
    //        return this;
    //     }

    //     // The 2-letter ISO 3166-1 code of the country you want to get headlines for. 
    //     // Possible options: us. 
    //     // Note: you can't mix this param with the sources param.
    //     public Builder setCountry(String country)
    //     {
    //         this.country = country;
    //         return this;
    //     }

    //     // Find sources that display news of this category. 
    //     // Possible options: business, entertainment, general, health, science, sports, technology. Default: all categories.
    //     public Builder setCategory(String category)
    //     {
    //          this.category = category;
    //          return this;
    //     }

    //     // A comma-seperated string of identifiers for the news sources or blogs you want headlines from. 
    //     // Use the /top-headlines/sources endpoint to locate these programmatically or look at the sources index. 
    //     // Note: you can't mix this param with the country or category params.
    //     public Builder setSource(String... sources)
    //     {
    //         // this.sources = sources;
    //         return this;
    //     }

    //     // Keywords or a phrase to search for.
    //     public Builder setKeywords(String keywords)
    //     {
    //         // Splits the keywords (ex. Trump and Epstein) and inserts a + in place of each space (Trump+and+Epstein).
    //         String[] splitKeywords = keywords.split(" ");
            
    //         for (String x : splitKeywords)
    //         {
    //             this.keywords = x + "+";
    //         }

    //         int index = this.keywords.lastIndexOf("+");
    //         this.keywords = this.keywords.substring(0, index);
    //         return this;
    //     }

    //     public NewsScraper buildNewsScraper()
    //     {
    //         return new NewsScraper(this);
    //     }  
    // }
}
