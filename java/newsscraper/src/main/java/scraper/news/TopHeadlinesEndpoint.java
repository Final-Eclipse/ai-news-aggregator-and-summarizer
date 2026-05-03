package scraper.news;
import java.util.HashMap;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;

public class TopHeadlinesEndpoint extends Endpoint
{
    // what data type to hold parameters
    // Add javadocs to all methods and builder methods.
    private String baseApiEndpointUrl = "https://newsapi.org/v2/top-headlines";
    
    private String country; // Can't be mixed with the sources parameter.
    private String category;    // Can't be mixed with the sources parameter.
    private List<String> sources = new ArrayList<>();   // Can't be mixed with country or category parameters.
    private String q;
    private String pageSize;
    private String page; 

    public TopHeadlinesEndpoint(Builder builder)
    {
        this.country = builder.country;
        this.category = builder.category;
        this.sources = builder.sources;
        this.q = builder.q;
        this.pageSize = builder.pageSize;
        this.page = builder.page;

        setApiEndpointUrl(baseApiEndpointUrl);
        addParametersToHashMap();
        appendQueryParameters();
    }

    public void addParametersToHashMap()
    {
        HashMap<String, Object> parametersHashMap = getParametersHashMap();

        parametersHashMap.put("country", country);
        parametersHashMap.put("category", category);
        parametersHashMap.put("sources", sources);
        parametersHashMap.put("q", q);
        parametersHashMap.put("pageSize", pageSize);
        parametersHashMap.put("page", page);

        setParametersHashMap(parametersHashMap);
    }

    public static class Builder
    {
        private String country; // Can't be mixed with the sources parameter.
        private String category;    // Can't be mixed with the sources parameter.
        private List<String> sources = new ArrayList<>();   // Can't be mixed with country or category parameters.
        private String q;
        private String pageSize;
        private String page; 

        public Builder()
        {
            
        }
        
        // Required, at least one.
        public Builder country(String country) { this.country = country; return this; }
        public Builder category(String category) { this.category = category; return this; }
        public Builder sources(String sources)
        {
            this.sources = splitCommaSeparatedString(sources);
            return this;
        }
        public Builder q(String q) { this.q = q; return this; }
        public Builder pageSize(String pageSize) { this.pageSize = pageSize; return this; }
        public Builder page(String page) { this.page = page; return this; }
        
        public TopHeadlinesEndpoint build()
        {
            if (country == null && category == null && sources == null && q == null && pageSize == null && page == null)
            {
                throw new NullPointerException("At least one of these parameters must not be null (country, category, sources, q, pageSize, page).");
            }
            else if ((country != null || category != null) && sources.size() != 0)
            {
                throw new IllegalArgumentException("Cannot mix the sources parameter with the country or category parameters.");
            }
            
            return new TopHeadlinesEndpoint(this);
        }

        // Returns an ArrayList containing the individual elements of a CSV input.
        // This is used for parameters that are able to be input as CSVs instead of just a single consistent string.
        private ArrayList<String> splitCommaSeparatedString(String input)
        {
            String[] splitArray = input.split("[,| ]+"); // Splits on commas and spaces.
            return new ArrayList<String>(Arrays.asList(splitArray));   
        }
    }
}
