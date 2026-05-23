package scraper.news;

import java.util.HashMap;

public class CreateEndpoint 
{
    private static Endpoint determineEndpoint(HashMap<String, String> endpointDataHashMap)
    {
        switch (endpointDataHashMap.get("endpoint"))
        {
            case "everything":
                return new EverythingEndpoint.Builder() 
                    .q(endpointDataHashMap.getOrDefault("q", null))
                    .searchIn(endpointDataHashMap.getOrDefault("searchIn", null))
                    .sources(endpointDataHashMap.getOrDefault("sources", null))
                    .domains(endpointDataHashMap.getOrDefault("domains", null))
                    .excludeDomains(endpointDataHashMap.getOrDefault("excludeDomains", null))
                    .from(endpointDataHashMap.getOrDefault("from", null))
                    .to(endpointDataHashMap.getOrDefault("to", null))
                    .language(endpointDataHashMap.getOrDefault("language", null))
                    .sortBy(endpointDataHashMap.getOrDefault("sortBy", null))
                    .pageSize(endpointDataHashMap.getOrDefault("pageSize", null))
                    .page(endpointDataHashMap.getOrDefault("page", null))
                    .build();

            case "top-headlines":
                // Assigns a default value to category.
                if (endpointDataHashMap.get("category").equals("null"))
                {
                    endpointDataHashMap.put("category", "general");
                }
                
                return new TopHeadlinesEndpoint.Builder()
                    .country(endpointDataHashMap.getOrDefault("country", null))
                    .category(endpointDataHashMap.getOrDefault("category", null))
                    .sources(endpointDataHashMap.getOrDefault("sources", null))
                    .q(endpointDataHashMap.getOrDefault("q", null))
                    .pageSize(endpointDataHashMap.getOrDefault("pageSize", null))
                    .page(endpointDataHashMap.getOrDefault("page", null))
                    .build();

            case "top-headlines/sources":
                return new SourcesEndpoint.Builder()
                    .category(endpointDataHashMap.getOrDefault("category", null))
                    .language(endpointDataHashMap.getOrDefault("language", null))
                    .country(endpointDataHashMap.getOrDefault("country", null))
                    .build();

            default:
                throw new IllegalArgumentException("Invalid endpoint type.");
        }
    }

    public static Endpoint create(HashMap<String, String> endpointDataHashMap)
    {
        return determineEndpoint(endpointDataHashMap);
    }

    // public EverythingEndpoint create()
    // {
        
    // }

    // public TopHeadlinesEndpoint create()
    // {

    // }

    // public SourcesEndpoint create()
    // {

    // }
}
