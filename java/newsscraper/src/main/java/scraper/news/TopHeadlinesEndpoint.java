package scraper.news;

// Have a parent Endpoint class that has general methods.
// Have each Endpoint child contain its specific methods.

public class TopHeadlinesEndpoint 
{
    private String apiKey;
    private String country;
    private String category;
    private String sources;
    private String q;
    private String pageSize;
    private String page;
}
