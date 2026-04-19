package scraper.news;
import java.util.HashMap;

// Have a parent Endpoint class that has general methods.
// Have each Endpoint child contain its specific methods.
// https://newsapi.org/docs/endpoints/everything

public class EverythingEndpoint 
{
    private String apiKey;
    private String apiEndpointUrl = "https://newsapi.org/v2/everything";

    // what data type to hold parameters
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
    // ainaas
    // ainas
    
    private HashMap<String, Object> parametersHashMap = new HashMap<String, Object>();

    // Use builder?
    // public EverythingEndpoint(String q, String searchIn, String[] sources, String[] domains, 
    //     String[] excludeDomains, String from, String to, String language, String sortBy, String pageSize, String page)
    // {
    //     this.q = q;
    //     this.searchIn = searchIn;
    //     this.sources = sources;
    //     this.domains = domains;
    //     this.excludeDomains = excludeDomains;
    //     this.from = from;
    //     this.to = to;
    //     this.language = language;
    //     this.sortBy = sortBy;
    //     this.pageSize = pageSize;
    //     this.page = page;
    // }

    public EverythingEndpoint(EverythingEndpointBuilder builder)
    {
        this.q = builder.q;
        this.searchIn = builder.searchIn;
        this.sources = builder.sources;
        this.domains = builder.domains;
        this.excludeDomains = builder.excludeDomains;
        this.from = builder.from;
        this.to = builder.to;
        this.language = builder.language;
        this.sortBy = builder.sortBy;
        this.pageSize = builder.pageSize;
        this.page = builder.page;

        addParametersToHashMap();

        for (Object x : parametersHashMap.keySet())
        {
            System.out.println(x + " : " + parametersHashMap.get(x));
        }
    }

    private void addParametersToHashMap()
    {
        parametersHashMap.put("q", q);
        parametersHashMap.put("searchIn", searchIn);
        parametersHashMap.put("sources", sources);
        parametersHashMap.put("domains", domains);
        parametersHashMap.put("excludeDomains", excludeDomains);
        parametersHashMap.put("from", from);
        parametersHashMap.put("to", to);
        parametersHashMap.put("language", language);
        parametersHashMap.put("sortBy", sortBy);
        parametersHashMap.put("pageSize", pageSize);
        parametersHashMap.put("page", page);
    }

    // Appends each query parameter to the API URL.
    // protected Endpoint appendQueryParameters()
    // {
    //     removeIncompatibleParameters();
    //     checkForNullParameters();
    //     checkForInvalidParameters();

    //     apiEndpointUrl = apiEndpointUrl + "?";

    //     for (String parameter : parametersHashMap.keySet())
    //     {
    //         endpointURL = endpointURL + parameter + "=" + parametersHashMap.get(parameter) + "&";
    //     }

    //     // Removes the last "&".
    //     int index = endpointURL.lastIndexOf("&");
    //     endpointURL = endpointURL.substring(0, index);

    //     return this;
    // }

    public static class EverythingEndpointBuilder
    {
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

        public EverythingEndpointBuilder()
        {
            
        }
        
        // Required, at least one.
        public EverythingEndpointBuilder q(String q) { this.q = q; return this; }
        public EverythingEndpointBuilder searchIn(String searchIn) { this.searchIn = searchIn; return this; }
        public EverythingEndpointBuilder sources(String... sources) { this.sources = sources; return this; }
        public EverythingEndpointBuilder domains(String... domains) { this.domains = domains; return this; }

        // Optional.
        public EverythingEndpointBuilder excludeDomains(String... domains) { this.excludeDomains = domains; return this; }
        public EverythingEndpointBuilder from(String from) { this.from = from; return this; }
        public EverythingEndpointBuilder to(String to) { this.to = to; return this; }
        public EverythingEndpointBuilder language(String language) { this.language = language; return this; }
        public EverythingEndpointBuilder sortBy(String sortBy) { this.sortBy = sortBy; return this; }
        public EverythingEndpointBuilder pageSize(String pageSize) { this.pageSize = pageSize; return this; }
        public EverythingEndpointBuilder page(String page) { this.page = page; return this; }
        
        public EverythingEndpoint build()
        {
            if (q == null && searchIn == null && sources == null && domains == null)
            {
                throw new NullPointerException("At least one of these must not be null (q, searchIn, sources, domains).");
            }
            
            return new EverythingEndpoint(this);
        }
    }
}
