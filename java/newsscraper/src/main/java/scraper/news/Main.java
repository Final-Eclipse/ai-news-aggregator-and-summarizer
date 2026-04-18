package scraper.news;

// Make a class that deals with each endpoint of the API.
// A class for /v2/everything, /v2/top-headlines, and /v2/top-headlines/sources.
// Or have one class that determines what the endpoint is and decides which logic to apply.

// Have one class for every endpoint.
// Have a HashMap for each endpoint that contains what the parameters of that endpoint is.
// Then, construct the URL for each parameter in the HashMap.
// private static Endpoint x = new Endpoint("everything")
// private static Endpoint x = new Endpoint("top-headlines")
// private static Endpoint x = new Endpoint("sources")
public class Main 
{
    // private static String apiURL = "https://newsapi.org/v2/everything";
    // private static String apiURL = "https://newsapi.org/v2/top-headlines";

    // To ignore certain values, set as null (.setCategory(null)).
    // private static NewsScraper newsScraper = new NewsScraper.Builder()
    //     .setApiURL(apiURL)
    //     .setCountry("US")
    //     .setCategory("general") 
    //     .buildNewsScraper();

    // private static NewsScraper newsScraper = new Builder();
    //     .setApiURL(apiURL)
    //     .setCountry("US")
    //     .setCategory("general") 
    //     .buildNewsScraper();

    public static void main(String[] args) 
    {
        // newsScraper.addQueryParameters();
        // newsScraper.getResponse();

        // For top-headlines, cannot have sources parameter as well as category or country.
        // Endpoint topHeadlines = new Endpoint("/v2/top-headlines", true)
        //     .addQueryParameterCategory("general")
        //     // .addQueryParameterLanguage("EN")  
        //     .addQueryParameterCountry("US") // country might need to be two letter length as well like language.
        //     .addQueryParameterSources("associated-press")   // Ensure that the overloaded constructor is used for the "/v2/top-headlines" endpoint and that sources = true.
        //     .addQueryParameterQ("iran")
        //     .addQueryParameterPageSize(100)
        //     .addQueryParameterPage(1)
        //     .appendQueryParameters();

        // System.out.println(x.apiURL);

        // NewsScraper y = new NewsScraper("https://newsapi.org/v2/everything");  
        // y.getResponse();
        // System.out.println(topHeadlines.getEndpointURL());

        //{"status":"ok","totalResults":8,"articles":[{"source":{"id":"the-washington-post","name":"The Washington Post"},
        // "author":"Scott Nover","title":"Judge rules Trump order eliminating NPR, PBS funding is unconstitutional - The Washington Post",
        // "description":"A federal judge struck down part of Trump?s order cutting NPR and PBS funding

        // test x = new test();
        // System.out.println(x);

        EverythingEndpoint x = new EverythingEndpoint.EverythingEndpointBuilder()
        .q("trump")
        .sources("AP News")
        .domains("")
        .excludeDomains("")
        .build();
        
    }
}