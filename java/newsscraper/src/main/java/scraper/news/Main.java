package scraper.news;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// Have one class for every endpoint.
// Have a HashMap for each endpoint that contains what the parameters of that endpoint is.
// Then, construct the URL for each parameter in the HashMap.
// private static Endpoint x = new Endpoint("everything")
// private static Endpoint x = new Endpoint("top-headlines")
// private static Endpoint x = new Endpoint("sources")

@SpringBootApplication
public class Main 
{
    private static String summarizationString;

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

        // // Arguments that contains spaces must be hyphenated (ex. associated press -> associated-press).
        // EverythingEndpoint x = new EverythingEndpoint.Builder()
        //     // Use URL encoding to add "%20" between spaces (ex. department of justice -> department%20of%20justice).
        //     // Wrap q in double quotes for exact phrase.
        //     // Can also use URL encoding to add double quotes (ex. united states -> %22united%20states%22).
        //     .q("trump")    // Add another boolean parameter, exactPhrase. Or detect if the user types double quotes and convert that if needed (ex. "\"south korea\"")
        //     .searchIn("title")
        //     .sources("associated-press")
        //     .domains("apnews.com, nbcnews.com")
        //     .excludeDomains("foxnews.com")
        //     .from("2026-04-20")
        //     .to("2026-04-24")
        //     .language("en")
        //     .sortBy(null)
        //     .pageSize("10")
        //     .page("1")
        //     .build();
        
        // TopHeadlinesEndpoint y = new TopHeadlinesEndpoint.Builder()
        //     .country("US")
        //     .category("general")
        //     // .sources("associated-press") // Can't mix the sources parameter with the country or category parameters.
        //     .q("trump")
        //     .pageSize("10")
        //     .page("1")
        //     .build();

        // SourcesEndpoint z = new SourcesEndpoint.Builder()
        //     .category("sports")
        //     .language("en")
        //     .country("us")
        //     .build();

        // NewsScraper newsScraper = new NewsScraper();

        // Sparkjava
        // get("/EverythingEndpoint", (request, response) -> newsScraper.getResponse(x.getApiEndpointUrl()));       
        // get("/TopHeadlinesEndpoint", (request, response) -> newsScraper.getResponse(y.getApiEndpointUrl()));       
        // get("/SourcesEndpoint", (request, response) -> newsScraper.getResponse(z.getApiEndpointUrl()));   
        
        // get("/Summarization", (request, response) -> summarizationString);
        // post("/Summarization", (request, response) -> { 
        //     summarizationString = request.body();
        //     return "Successful Post";
        // });   

        // mvn spring-boot:run
        // or
        // .\/mvnw.cmd spring-boot:run
        // Spring Boot
        SpringApplication.run(Main.class, args);
    }
}