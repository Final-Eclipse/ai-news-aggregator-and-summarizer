package scraper.news;
import java.util.HashMap;
import java.util.List;

public abstract class Endpoint 
{
    // public String q;
    // public List<String> searchIn = new ArrayList<>();
    // public List<String> sources = new ArrayList<>();
    // public List<String> domains = new ArrayList<>();
    // public List<String> excludeDomains = new ArrayList<>();
    // public String from;
    // public String to;
    // public String language;
    // public String sortBy;
    // public String pageSize;
    // public String page; 

    private String apiEndpointUrl;
    private HashMap<String, Object> parametersHashMap = new HashMap<String, Object>();

    public abstract void addParametersToHashMap();

    // Appends each query parameter to the API URL.
    // Uses appendCSVQueryParameters() as a helper method.
    public void appendQueryParameters()
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

    public HashMap<String, Object> getParametersHashMap()
    {
        return parametersHashMap;
    }

    public void setParametersHashMap(HashMap<String, Object> parametersHashMap)
    {
        this.parametersHashMap = parametersHashMap;
    }

    public String getApiEndpointUrl()
    {
        return apiEndpointUrl;
    }

    public void setApiEndpointUrl(String apiEndpointUrl)
    {
        this.apiEndpointUrl = apiEndpointUrl;
    }
}
