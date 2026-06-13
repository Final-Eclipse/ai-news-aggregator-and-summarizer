package scraper.news.services;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;
import java.util.List;

// Use StringBuilder for more efficiency versus String concatenation?
public abstract class EndpointService
{
    private String apiEndpointUrl;
    private HashMap<String, Object> parametersHashMap = new HashMap<String, Object>();
    private final Set<String> specialQueryParameters = Set.of("searchIn", "sources", "domains", "excludeDomains");

    /**
     * Abstract method that must be implemented by children classes.
     * It must use the methods getParametersHashMap() and setParametersHashMap()
     * in order to update the parametersHashMap in this file.
     */
    public abstract void addParametersToHashMap();

    /**
     * Appends each query parameter in parametersHashMap to the apiEndpointUrl.
     */
    public void appendQueryParameters()
    {
        apiEndpointUrl += "?";

        for (String queryParameter : parametersHashMap.keySet())
        {
            Object value = parametersHashMap.get(queryParameter);
            if (isValueNullOrEmpty(value) == true)
            {
                continue;
            }
            
            apiEndpointUrl += queryParameter + "=";
            if (specialQueryParameters.contains(queryParameter))
            {
                value = getCsvQueryParameters(value);
            }
            else if (((String) value).contains(" "))
            {
                value = encodeQueryParameterSpaces((String) value);
            }

            apiEndpointUrl += value + "&";
        }

        truncateUrl(1);
    }

    /**
     * Returns a boolean based on whether or not the parameter is null or empty.
     * 
     * @param value An Object that corresponds with its query parameter key.
     * @return boolean true if value is null or empty; false otherwise.
     */
    private boolean isValueNullOrEmpty(Object value)
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
            return ((List<?>) value).isEmpty();
        }
        else
        {
            return false;
        }
    }

    /**
     * Converts the parameter to a List<String>, 
     * then to a single String and appends it to the apiEndpointUrl.
     * 
     * @param csvValues An Object of csvValues.
     */
    private String getCsvQueryParameters(Object csvValues)
    {
        List<String> csvList = getListOfStrings(csvValues);
        return getCsvString(csvList);
    }

    /**
     * Converts an Object parameter to a List and returns it.
     * 
     * @param csvValues An Object that is mapped to a List<String>.
     * @return List<String> made up of csvValues' elements.
     */
    private List<String> getListOfStrings(Object csvValues)
    {
        List<String> newList = new ArrayList<String>();
        for (Object x : (List<?>) csvValues)
        {
            if (x instanceof String)
            {
                newList.add((String) x);
            }
        }

        return newList;
    }

    /**
     * Takes a List<String> and combines its elements into one String
     * separated by commas and returns it.
     * 
     * @param csvList A List<String> whose elements are to be separated by commas.
     * @return String of each element of csvList separated by commas with no spaces.
     */
    private String getCsvString(List<String> csvList)
    {
        String csvString = "";
        for (String element : csvList)
        {
            csvString = csvString + element + ",";   
        }

        csvString = csvString.substring(0, csvString.length() - 1);
        return csvString;
    }

    /**
     * Encodes spaces as "%20" for the given queryParameter.
     * 
     * @param queryParameter The query parameter to encode spaces in.
     * @return String of the query parameters but with encoded spaces.
     */
    private String encodeQueryParameterSpaces(String queryParameter)
    {
        String[] splitArray = queryParameter.split(" ");
        String encodedQueryParameter = "";

        for (String x : splitArray)
        {
            encodedQueryParameter += x + "%20";
        }

        encodedQueryParameter = encodedQueryParameter.substring(0, encodedQueryParameter.length() - 3);
        encodedQueryParameter = encodeDoubleQuotes(encodedQueryParameter);
        return encodedQueryParameter;
    }

    /**
     * Encodes the given queryParameter with double quotes.
     * Mainly used for the query parameter "q" in order to search for exact phrases instead of a single word.
     * 
     * @param queryParameter The query parameter to encode in surrounding double quotes.
     * @return String of the double quote encoded queryParameter.
     */
    private String encodeDoubleQuotes(String queryParameter)
    {
        return "%22" + queryParameter + "%22";
    }
    
    /**
     * Removes the last character of the apiEndpointUrl.
     * This is useful in cases where there may be an "&" or "," at the end of the string, 
     * after appending query parameters.
     *
     * @param elementsToTruncate Number of characters to remove from the end of the apiEndpointUrl.
     */
    private void truncateUrl(int elementsToTruncate)
    {
        apiEndpointUrl = apiEndpointUrl.substring(0, apiEndpointUrl.length() - elementsToTruncate);
    }

    // Getters
    public HashMap<String, Object> getParametersHashMap()
    {
        return parametersHashMap;
    }

    public String getApiEndpointUrl()
    {
        return apiEndpointUrl;
    }

    // Setters
    public void setParametersHashMap(HashMap<String, Object> parametersHashMap)
    {
        this.parametersHashMap = parametersHashMap;
    }

    public void setApiEndpointUrl(String apiEndpointUrl)
    {
        this.apiEndpointUrl = apiEndpointUrl;
    }
}
