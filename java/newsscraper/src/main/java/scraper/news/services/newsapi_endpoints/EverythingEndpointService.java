package scraper.news.services.newsapi_endpoints;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import scraper.news.services.BaseEndpointService;

public class EverythingEndpointService extends BaseEndpointService
{
    private final String baseApiEndpointUrl = "https://newsapi.org/v2/everything";
    
    // At least one is required.
    private String q;
    private List<String> searchIn = new ArrayList<>();
    private List<String> sources = new ArrayList<>();
    private List<String> domains = new ArrayList<>();
    private List<String> excludeDomains = new ArrayList<>();

    // Optional
    private String from;
    private String to;
    private String language;
    private String sortBy;
    private String pageSize;
    private String page; 

    public EverythingEndpointService(Builder builder)
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

        setApiEndpointUrl(baseApiEndpointUrl);
        addParametersToHashMap();
        appendQueryParameters();
    }

    /**
     * Updates the parent's parametersHashMap with new keys and values.
     */
    @Override
    public void addParametersToHashMap()
    {
        HashMap<String, Object> parametersHashMap = getParametersHashMap();

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

        setParametersHashMap(parametersHashMap);
    }

    public static class Builder
    {
        private String q;
        private List<String> searchIn = new ArrayList<>();
        private List<String> sources = new ArrayList<>();
        private List<String> domains = new ArrayList<>();
        private List<String> excludeDomains = new ArrayList<>();
        private String from;
        private String to;
        private String language;
        private String sortBy;
        private String pageSize;
        private String page; 

        public Builder()
        {
            
        }
        
        // At least one is required.
        public Builder q(String q) { this.q = q; return this; }
        public Builder searchIn(String searchIn) 
        { 
            this.searchIn = splitCommaSeparatedString(searchIn); 
            return this; 
        }
        public Builder sources(String sources) 
        { 
            this.sources = splitCommaSeparatedString(sources); 
            return this; 
        }
        public Builder domains(String domains) 
        { 
            this.domains = splitCommaSeparatedString(domains); 
            return this; 
        }

        // Optional.
        public Builder excludeDomains(String domains) 
        { 
            this.excludeDomains = splitCommaSeparatedString(domains); 
            return this; 
        }
        public Builder from(String from) { this.from = from; return this; }   // Must be in ISO 8601 format (2026-04-20T00:00:00).
        public Builder to(String to) { this.to = to; return this; }   // Must be in ISO 8601 format (2026-04-20T00:00:00).
        public Builder language(String language) { this.language = language; return this; }
        public Builder sortBy(String sortBy) { this.sortBy = sortBy; return this; }
        public Builder pageSize(String pageSize) { this.pageSize = pageSize; return this; }
        public Builder page(String page) { this.page = page; return this; }
        
        public EverythingEndpointService build()
        {
            if (q == null && searchIn == null && sources == null && domains == null)
            {
                throw new NullPointerException("At least one of these parameters must not be null (q, searchIn, sources, domains).");
            }
            
            return new EverythingEndpointService(this);
        }

        /**
         * Splits elements of a csvString into an ArrayList<String>.
         * 
         * @param csvString String of comma-separated values.
         * @return ArrayList<String> containing elements of csvString.
         */
        private ArrayList<String> splitCommaSeparatedString(String csvString)
        {
            if (csvString == null)
            {
                return null;
            }

            String[] splitArray = csvString.split("[,| ]+"); // Splits on commas and spaces.
            return new ArrayList<String>(Arrays.asList(splitArray));   
        }
    }
}
