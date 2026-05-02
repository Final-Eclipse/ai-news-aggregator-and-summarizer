// package scraper.news;
// import java.util.HashMap;
// import java.util.List;
// import java.util.Arrays;
// import java.util.ArrayList;

// public class TopHeadlinesEndpoint 
// {
//     private String apiEndpointUrl = "https://newsapi.org/v2/top-headlines";

//     // what data type to hold parameters
//     // Add javadocs to all methods and builder methods.
//     private String country; // Can't be mixed with the sources parameter.
//     private String category;    // Can't be mixed with the sources parameter.
//     private List<String> sources = new ArrayList<>();   // Can't be mixed with country or category parameters.
//     private String q;
//     private String pageSize;
//     private String page; 
    
//     private HashMap<String, Object> parametersHashMap = new HashMap<String, Object>();

//     public TopHeadlinesEndpoint(TopHeadlinesEndpointBuilder builder)
//     {
//         this.country = builder.country;
//         this.category = builder.category;
//         this.sources = builder.sources;
//         this.q = builder.q;
//         this.pageSize = builder.pageSize;
//         this.page = builder.page;

//         addParametersToHashMap();
//         appendQueryParameters();

//         // for (Object x : parametersHashMap.keySet())
//         // {
//         //     // System.out.println(x + " : " + parametersHashMap.get(x));
//         // }
//     }

//     private void addParametersToHashMap()
//     {
//         parametersHashMap.put("country", country);
//         parametersHashMap.put("category", category);
//         parametersHashMap.put("sources", sources);
//         parametersHashMap.put("q", q);
//         parametersHashMap.put("pageSize", pageSize);
//         parametersHashMap.put("page", page);
//     }

//     // Appends each query parameter to the API URL.
//     // Uses appendCSVQueryParameters() as a helper method.
//     private void appendQueryParameters()
//     {
//         apiEndpointUrl = apiEndpointUrl + "?";

//         for (String queryParameter : parametersHashMap.keySet())
//         {
//             Object value = parametersHashMap.get(queryParameter);
//             if (isQueryParameterNullOrEmpty(value) == true)
//             {
//                 continue;
//             }
//             else
//             {
//                 apiEndpointUrl += queryParameter + "=";
//             }

//             if (queryParameter.equals("sources"))
//             {
//                 appendCsvQueryParameters(value);
//                 truncateUrl(1);
//                 apiEndpointUrl = apiEndpointUrl + "&";
//             }
//             else
//             {  
//                 if (((String) value).contains(" "))
//                 {
//                     value = encodeQueryParameterSpaces((String) value);
//                     apiEndpointUrl += value + "&";
//                 }
//                 else
//                 {
//                     apiEndpointUrl += value + "&";
//                 }
//             }
//         }

//         truncateUrl(1);
//         System.out.println(apiEndpointUrl);
//     }

//     // Returns a boolean after checking if the value parameter is null or empty.
//     private boolean isQueryParameterNullOrEmpty(Object value)
//     {
//         if (value == null)
//         {
//             return true;
//         }
//         else if (value instanceof String)
//         {
//             return value.equals("");
//         }
//         else if (value instanceof List)
//         {
//             List<String> searchInList = (List<String>) value;
//             return searchInList.isEmpty();
//         }
//         else
//         {
//             return false;
//         }
//     }

//     // Only used and called from within appendQueryParameters().
//     private void appendCsvQueryParameters(Object value)
//     {
//         List<String> searchInList = (List<String>) value;
//         apiEndpointUrl += getCsvString(searchInList);
//     }

//     // Only used and called from within appendCSVQueryParameters().
//     private String getCsvString(List<String> searchInList)
//     {
//         String csvString = "";
//         for (String element : searchInList)
//         {
//             csvString = csvString + element + ",";   
//         }

//         return csvString;
//     }

//     private String encodeQueryParameterSpaces(String queryParameter)
//     {
//         String[] splitArray = queryParameter.split(" ");
//         String newString = "";

//         for (String x : splitArray)
//         {
//             newString += x + "%20";
//         }

//         newString = newString.substring(0, newString.length() - 3);
//         return newString;
//     }

//     // Removes the last character of the apiEndpointUrl.
//     // This is useful in cases where there may be an "&" or "," at the end of the string,
//     // after appending query parameters.
//     private void truncateUrl(int elementsToTruncate)
//     {
//         apiEndpointUrl = apiEndpointUrl.substring(0, apiEndpointUrl.length() - elementsToTruncate);
//     }

//     public static class TopHeadlinesEndpointBuilder
//     {
//         private String q;
//         private List<String> searchIn = new ArrayList<>();
//         private List<String> sources = new ArrayList<>();
//         private List<String> domains = new ArrayList<>();
//         private List<String> excludeDomains = new ArrayList<>();
//         private String from;
//         private String to;
//         private String language;
//         private String sortBy;
//         private String pageSize;
//         private String page; 

//         public TopHeadlinesEndpointBuilder()
//         {
            
//         }
        
//         // Required, at least one.
//         public TopHeadlinesEndpointBuilder q(String q) { this.q = q; return this; }
//         public TopHeadlinesEndpointBuilder searchIn(String searchIn) 
//         { 
//             this.searchIn = splitCommaSeparatedString(searchIn); 
//             return this; 
//         }
//         public TopHeadlinesEndpointBuilder sources(String sources) 
//         { 
//             this.sources = splitCommaSeparatedString(sources); 
//             return this; 
//         }
//         public TopHeadlinesEndpointBuilder domains(String domains) 
//         { 
//             this.domains = splitCommaSeparatedString(domains); 
//             return this; 
//         }

//         // Optional.
//         public TopHeadlinesEndpointBuilder excludeDomains(String domains) 
//         { 
//             this.excludeDomains = 
//             splitCommaSeparatedString(domains); 
//             return this; 
//         }
//         /**
//          * The starting date for which articles must be from.
//          * @param from A date in ISO 8601 format (2026-04-20T00:00:00).
//          * @return TopHeadlinesEndpointBuilder
//          */
//         public TopHeadlinesEndpointBuilder from(String from) { this.from = from; return this; }   // from
//         public TopHeadlinesEndpointBuilder to(String to) { this.to = to; return this; }   // to=2026-04-20T00:00:00
//         public TopHeadlinesEndpointBuilder language(String language) { this.language = language; return this; }
//         public TopHeadlinesEndpointBuilder sortBy(String sortBy) { this.sortBy = sortBy; return this; }
//         public TopHeadlinesEndpointBuilder pageSize(String pageSize) { this.pageSize = pageSize; return this; }
//         public TopHeadlinesEndpointBuilder page(String page) { this.page = page; return this; }
        
//         public TopHeadlinesEndpoint build()
//         {
//             if (q == null && searchIn == null && sources == null && domains == null)
//             {
//                 throw new NullPointerException("At least one of these parameters must not be null (q, searchIn, sources, domains).");
//             }
            
//             return new TopHeadlinesEndpoint(this);
//         }

//         // Returns an ArrayList containing the individual elements of a CSV input.
//         // This is used for parameters that are able to be input as CSVs instead of just a single consistent string.
//         private ArrayList<String> splitCommaSeparatedString(String input)
//         {
//             String[] splitArray = input.split("[,| ]+"); // Splits on commas and spaces.
//             return new ArrayList<String>(Arrays.asList(splitArray));   
//         }
//     }
// }
