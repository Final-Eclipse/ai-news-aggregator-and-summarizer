package scraper.news;

// Have a parent Endpoint class that has general methods.
// Have each Endpoint child contain its specific methods.
// https://newsapi.org/docs/endpoints/everything

public class EverythingEndpoint 
{
    private String apiKey;
    private String q;
    private String searchIn;
    private String[] sources;
    private String[] domains;
    private String[] excludeDomains;
    private String from;
    private String to;
    private String language;
    private String sortBy;
    private String pageSize;
    private String page; 
}
