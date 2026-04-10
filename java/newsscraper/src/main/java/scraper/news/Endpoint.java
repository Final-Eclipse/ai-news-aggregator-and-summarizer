package scraper.news;
import java.util.HashMap;
import java.util.Arrays;
import java.util.ArrayList;

public class Endpoint
{
    private String apiURL = "https://newsapi.org";
    private String endpointURL;
    private String endpoint;
    private boolean sources;

    private HashMap<String, String> parametersHashMap = new HashMap<String, String>();

    private String[] everythingParametersArray = {"q", "searchIn", "sources", "domains", 
    "excludeDomains", "from", "to", "language", "sortBy", "pageSize", "page"};

    private String[] topHeadlinesParametersArray = {"country", "category", "sources",
    "q", "pageSize", "page"};
    // private String[] topHeadlinesParametersArray = {"country", "category", "sources", 
    // "q", "pageSize", "page"};

    private String[] sourcesParametersArray = {"category", "language", "country"};

    private String[][] parametersArray = {everythingParametersArray, topHeadlinesParametersArray, sourcesParametersArray};

    public Endpoint2(String endpoint)
    {
        this.endpoint = endpoint;

        initializeParameters();    
        generateEndpointURL();
    }

    // Serves the same purpose as the single parameter constructor.
    // However, if it is given the "/v2/top-headlines" endpoint,
    // it will automatically remove the "country" and "category" parameters if "sources" == true.
    public Endpoint2(String endpoint, boolean sources)
    {
        this.endpoint = endpoint;
        this.sources = sources;
        
        initializeParameters();
        generateEndpointURL();
    }

    protected String getEndpointURL()
    {
        return endpointURL;
    }
    
    // Possible options include: business, entertainment, health, science, sports, and technology.
    public Endpoint2 addQueryParameterCategory(String category)
    {
        // checkForInvalidParameter("category");
        parametersHashMap.put("category", category);
        return this;
    }

    // Language needs to be a two letter string (EN, FR, ES).
    public Endpoint2 addQueryParameterLanguage(String language)
    { 
        // checkForInvalidParameter("language");
        // parametersHashMap.remove("sources");
        parametersHashMap.put("language", language);    // do i need to initialize the hashmap at top of file if i am adding the key here anyways?
        return this;
    }

    public Endpoint2 addQueryParameterCountry(String country)
    {
        // checkForInvalidParameter("country");
        // parametersHashMap.remove("sources");
        parametersHashMap.put("country", country);
        return this;
    }

    // Sources is a comma separated string.
    public Endpoint2 addQueryParameterSources(String... sources)
    {
        // checkForInvalidParameter("sources");
        // parametersHashMap.remove("country");
        // parametersHashMap.remove("category");
        parametersHashMap.put("sources", sources[0]);
        return this;
    }

    public Endpoint2 addQueryParameterQ(String q)
    {
        // checkForInvalidParameter("q");
        parametersHashMap.put("q", q);
        return this;
    }

    public Endpoint2 addQueryParameterPageSize(int pageSize)
    {
        // checkForInvalidParameter("pageSize");
        parametersHashMap.put("pageSize", String.valueOf(pageSize));
        return this;
    }

    public Endpoint2 addQueryParameterPage(int page)
    {
        // checkForInvalidParameter("page");
        parametersHashMap.put("page", String.valueOf(page));
        return this;
    }

    // Returns a 2D array that contains the parameters for the given endpoint.
    private String[] getParametersForEndpoint()
    {
        int index = switch (endpoint)
        {
            case "/v2/everything" -> 0;
            case "/v2/top-headlines" -> 1;
            case "/v2/top-headlines/sources" -> 2;
            default -> -1;
        };

        return parametersArray[index];
    }

    // Initializes the parametersHashMap with each key being a parameter of the endpoint. 
    private void initializeParameters()
    {
        String[] parameters = getParametersForEndpoint();

        for (String parameter : parameters)
        {
            parametersHashMap.put(parameter, null);
        }
    }

    // Appends the endpoint path to the API URL.
    private void generateEndpointURL()
    {
        endpointURL = apiURL + this.endpoint;
    }

    // Checks for parameters that are not valid with the selected endpoint.
    // Throws an exception if an invalid parameter is found.
    // Maybe check if a parameter was added that is not for this specific endpoint.
    // Ex. pageSize parameter for the sources endpoint does not exist, so throw an exception.
    private void checkForInvalidParameters()
    {
        ArrayList<String> invalidParameters = new ArrayList<String>();
        String[] validParameters = getParametersForEndpoint();

        for (String parameter : parametersHashMap.keySet())
        {
            if (Arrays.asList(validParameters).contains(parameter) == false)
            {
                invalidParameters.add(parameter);
            }
        }
        
        if (invalidParameters.size() > 0)
        {
            throw new IllegalArgumentException("The parameter(s), \"" + invalidParameters.toString() + "\", are not needed for the \"" + endpoint + "\" endpoint.");
        }

        // Only applies to the endpoint /v2/top-headlines.
        // Throws an exception if the "sources" parameter is used with the "country" or "category" parameters.
        // It is not allowed by the NewsAPI.
        if (parametersHashMap.containsKey("sources") && (parametersHashMap.containsKey("country") || parametersHashMap.containsKey("category")))
        {
            throw new IllegalArgumentException("The parameter, \"sources\", cannot be used with the country or category parameters.");
        }
    }

    // Removes incompatible parameters.
    // Ex. "sources" with "country" or "category" as this is not allowed for the "/v2/top-headlines" endpoint.
    private void removeIncompatibleParameters()
    {
        if (!endpoint.equals("/v2/top-headlines"))
        {
            return;
        }
        else if (sources == true)
        {
            parametersHashMap.remove("country");
            parametersHashMap.remove("category");
        }
        else if (sources == false)
        {
            parametersHashMap.remove("sources");
        }
    }

    // Removes parameters that should not be together.
    // Ex. sources and country or category
    // This method would remove the country and category if sources != null.
    // This method would remove sources if country and category != null.
    // private void removeIncompatibleParameters()
    // {
    //     if (!endpointURL.equals("https://newsapi.org/v2/top-headlines"))
    //     {
    //         return;
    //     }

    //     if (parametersHashMap.get("sources") == null && parametersHashMap.get("country") != null && parametersHashMap.get("category") != null)
    //     {
    //     // for (String x : parametersHashMap.keySet())
    //     //     {
    //     //         System.out.println(x);
    //     //     }
    //         // System.out.println();
    //         // System.out.println("ajiodjoidajso");
    //         parametersHashMap.remove("sources");

    //         // for (String x : parametersHashMap.keySet())
    //         // {
    //         //     System.out.println(x);
    //         // }
    //     }
    //     else
    //     {
    //         parametersHashMap.remove("country");
    //         parametersHashMap.remove("category");
    //     }
    //     // ArrayList<String> newArrayList = new ArrayList<String>();

    //     // for (String parameter : parametersHashMap.keySet())
    //     // {
    //     //     if (parametersHashMap.get(parameter) != null)
    //     //     {
    //     //         // parametersHashMap.remove(parameter);
    //     //         newArrayList.add(parameter);
    //     //     }
    //     // }

    //     // parametersHashMap.clear();
    //     // for (String parameter : newArrayList)
    //     // {
    //     //     parametersHashMap.put(parameter);
    //     // }
    // }

    // Change addQueryParameterSources() and other methods to just setSources, setCountry, etc.
    // In those methods, append the argument to an array.
    // In this method, set each key in the parametersHashMap to its corresponding value after checking if
    // the key is a valid parameter in checkForInvalidParameter().
    // private void addQueryParameters()
    // {

    // }

    // Checks the Endpoint's parametersHashMap for any null values.
    // Maybe check if a parameter was added that is not for this specific endpoint.
    // Ex. pageSize parameter for the sources endpoint does not exist, so throw an exception.
    private void checkForNullParameters()
    {
        ArrayList<String> nullParametersList = new ArrayList<String>();

        for (String parameter : parametersHashMap.keySet())
        {
            if (parametersHashMap.get(parameter) == null)
            {
                nullParametersList.add(parameter);
            }
        }
        
        if (nullParametersList.size() > 0)
        {
            throw new IllegalArgumentException("The parameter(s), " + nullParametersList.toString() + ", do not have values.");
        }
    }

    // Appends each query parameter to the API URL.
    protected Endpoint2 appendQueryParameters()
    {
        removeIncompatibleParameters();
        checkForNullParameters();
        checkForInvalidParameters();

        endpointURL = endpointURL + "?";

        for (String parameter : parametersHashMap.keySet())
        {
            endpointURL = endpointURL + parameter + "=" + parametersHashMap.get(parameter) + "&";
        }

        // Removes the last "&".
        int index = endpointURL.lastIndexOf("&");
        endpointURL = endpointURL.substring(0, index);

        return this;
    }
}    