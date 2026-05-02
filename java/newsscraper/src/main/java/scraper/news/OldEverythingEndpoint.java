package scraper.news;
import java.util.HashMap;
import java.util.List;
import java.util.Arrays;
import java.util.ArrayList;

// Have a parent Endpoint class that has general methods.
// Have each Endpoint child contain its specific methods.
// https://newsapi.org/docs/endpoints/everything

public class OldEverythingEndpoint 
{
    private String apiEndpointUrl = "https://newsapi.org/v2/everything";

    // what data type to hold parameters
    // Add javadocs to all methods and builder methods.
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
    
    private HashMap<String, Object> parametersHashMap = new HashMap<String, Object>();

    public OldEverythingEndpoint(EverythingEndpointBuilder builder)
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
        appendQueryParameters();

        // for (Object x : parametersHashMap.keySet())
        // {
        //     // System.out.println(x + " : " + parametersHashMap.get(x));
        // }
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
    // Uses appendCSVQueryParameters() as a helper method.
    private void appendQueryParameters()
    {
        apiEndpointUrl = apiEndpointUrl + "?";

        for (String queryParameter : parametersHashMap.keySet())
        {
            Object value = parametersHashMap.get(queryParameter);
            if (isQueryParameterNullOrEmpty(value) == true)
            {
                continue;
            }
            else
            {
                apiEndpointUrl += queryParameter + "=";
            }

            if (queryParameter.equals("searchIn") || queryParameter.equals("sources") || queryParameter.equals("domains") || queryParameter.equals("excludeDomains"))
            {
                appendCsvQueryParameters(value);
                truncateUrl(1);
                apiEndpointUrl = apiEndpointUrl + "&";
            }
            else
            {  
                if (((String) value).contains(" "))
                {
                    value = encodeQueryParameterSpaces((String) value);
                    apiEndpointUrl += value + "&";
                }
                else
                {
                    apiEndpointUrl += value + "&";
                }
            }
        }

        truncateUrl(1);
        System.out.println(apiEndpointUrl);
    }

    // Returns a boolean after checking if the value parameter is null or empty.
    private boolean isQueryParameterNullOrEmpty(Object value)
    {
        if (value == null)
        {
            return true;
        }
        else if (value instanceof String)
        {
            return value.equals("");
        }
        else if (value instanceof List)
        {
            List<String> searchInList = (List<String>) value;
            return searchInList.isEmpty();
        }
        else
        {
            return false;
        }
    }

    // Only used and called from within appendQueryParameters().
    private void appendCsvQueryParameters(Object value)
    {
        List<String> searchInList = (List<String>) value;
        apiEndpointUrl += getCsvString(searchInList);
    }

    // Only used and called from within appendCSVQueryParameters().
    private String getCsvString(List<String> searchInList)
    {
        String csvString = "";
        for (String element : searchInList)
        {
            csvString = csvString + element + ",";   
        }

        return csvString;
    }

    private String encodeQueryParameterSpaces(String queryParameter)
    {
        String[] splitArray = queryParameter.split(" ");
        String newString = "";

        for (String x : splitArray)
        {
            newString += x + "%20";
        }

        newString = newString.substring(0, newString.length() - 3);
        newString = encodeDoubleQuotes(newString);
        return newString;
    }

    // Encodes the API URL with double quotes.
    // This will cause the News API to look for that exact phrase instead of any of those words.
    private String encodeDoubleQuotes(String newString)
    {
        return "%22" + newString + "%22";
    }

    // Removes the last character of the apiEndpointUrl.
    // This is useful in cases where there may be an "&" or "," at the end of the string,
    // after appending query parameters.
    private void truncateUrl(int elementsToTruncate)
    {
        apiEndpointUrl = apiEndpointUrl.substring(0, apiEndpointUrl.length() - elementsToTruncate);
    }

    public static class EverythingEndpointBuilder
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

        public EverythingEndpointBuilder()
        {
            
        }
        
        // Required, at least one.
        public EverythingEndpointBuilder q(String q) { this.q = q; return this; }
        public EverythingEndpointBuilder searchIn(String searchIn) 
        { 
            this.searchIn = splitCommaSeparatedString(searchIn); 
            return this; 
        }
        public EverythingEndpointBuilder sources(String sources) 
        { 
            this.sources = splitCommaSeparatedString(sources); 
            return this; 
        }
        public EverythingEndpointBuilder domains(String domains) 
        { 
            this.domains = splitCommaSeparatedString(domains); 
            return this; 
        }

        // Optional.
        public EverythingEndpointBuilder excludeDomains(String domains) 
        { 
            this.excludeDomains = 
            splitCommaSeparatedString(domains); 
            return this; 
        }
        /**
         * The starting date for which articles must be from.
         * @param from A date in ISO 8601 format (2026-04-20T00:00:00).
         * @return EverythingEndpointBuilder
         */
        public EverythingEndpointBuilder from(String from) { this.from = from; return this; }   // from
        public EverythingEndpointBuilder to(String to) { this.to = to; return this; }   // to=2026-04-20T00:00:00
        public EverythingEndpointBuilder language(String language) { this.language = language; return this; }
        public EverythingEndpointBuilder sortBy(String sortBy) { this.sortBy = sortBy; return this; }
        public EverythingEndpointBuilder pageSize(String pageSize) { this.pageSize = pageSize; return this; }
        public EverythingEndpointBuilder page(String page) { this.page = page; return this; }
        
        public OldEverythingEndpoint build()
        {
            if (q == null && searchIn == null && sources == null && domains == null)
            {
                throw new NullPointerException("At least one of these parameters must not be null (q, searchIn, sources, domains).");
            }
            
            return new OldEverythingEndpoint(this);
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
