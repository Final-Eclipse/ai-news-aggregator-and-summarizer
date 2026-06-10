package scraper.news.services;

import scraper.news.models.Endpoint;
import scraper.news.models.dtos.EndpointDto;
import scraper.news.services.newsapi_endpoints.EverythingEndpoint;
import scraper.news.services.newsapi_endpoints.SourcesEndpoint;
import scraper.news.services.newsapi_endpoints.TopHeadlinesEndpoint;

public class CreateEndpoint 
{
    public static Endpoint create(EndpointDto endpointData)
    {
        switch (endpointData.getEndpoint())
        {
            case "everything":
                return createEverythingEndpoint(endpointData);
                
            case "top-headlines":
                return createTopHeadlinesEndpoint(endpointData);
                
            case "top-headlines/sources":
                return createSourcesEndpoint(endpointData);

            default:
                throw new IllegalArgumentException("Invalid endpoint type.");
        }
    }

    private static EverythingEndpoint createEverythingEndpoint(EndpointDto endpointData)
    {
        return new EverythingEndpoint.Builder() 
            .q(endpointData.getQ())
            .searchIn(endpointData.getSearchIn())
            .sources(endpointData.getSources())
            .domains(endpointData.getDomains())
            .excludeDomains(endpointData.getExcludeDomains())
            .from(endpointData.getFrom())
            .to(endpointData.getTo())
            .language(endpointData.getLanguage())
            .sortBy(endpointData.getSortBy())
            .pageSize(endpointData.getPageSize())
            .page(endpointData.getPage())
            .build();
    }

    private static TopHeadlinesEndpoint createTopHeadlinesEndpoint(EndpointDto endpointData)
    {
        return new TopHeadlinesEndpoint.Builder()
            .country(endpointData.getCountry())
            .category(endpointData.getCategory())
            .sources(endpointData.getSources())
            .q(endpointData.getQ())
            .pageSize(endpointData.getPageSize())
            .page(endpointData.getPage())
            .build();
    }

    private static SourcesEndpoint createSourcesEndpoint(EndpointDto endpointData)
    {
        return new SourcesEndpoint.Builder()
            .category(endpointData.getCategory())
            .language(endpointData.getLanguage())
            .country(endpointData.getCountry())
            .build();
    }

    // ========================
    // ========================
    // ========================
    // ========================
    // ========================

    // public static Endpoint create(HashMap<String, String> endpointDataHashMap)
    // {
    //     switch (endpointDataHashMap.get("endpoint"))
    //     {
    //         case "everything":
    //             return createEverythingEndpoint(endpointDataHashMap);
                
    //         case "top-headlines":
    //             return createTopHeadlinesEndpoint(endpointDataHashMap);
                
    //         case "top-headlines/sources":
    //             return createSourcesEndpoint(endpointDataHashMap);

    //         default:
    //             throw new IllegalArgumentException("Invalid endpoint type.");
    //     }
    // }

    // private static EverythingEndpoint createEverythingEndpoint(HashMap<String, String> endpointDataHashMap)
    // {
    //     return new EverythingEndpoint.Builder() 
    //         .q(endpointDataHashMap.getOrDefault("q", null))
    //         .searchIn(endpointDataHashMap.getOrDefault("searchIn", null))
    //         .sources(endpointDataHashMap.getOrDefault("sources", null))
    //         .domains(endpointDataHashMap.getOrDefault("domains", null))
    //         .excludeDomains(endpointDataHashMap.getOrDefault("excludeDomains", null))
    //         .from(endpointDataHashMap.getOrDefault("from", null))
    //         .to(endpointDataHashMap.getOrDefault("to", null))
    //         .language(endpointDataHashMap.getOrDefault("language", null))
    //         .sortBy(endpointDataHashMap.getOrDefault("sortBy", null))
    //         .pageSize(endpointDataHashMap.getOrDefault("pageSize", null))
    //         .page(endpointDataHashMap.getOrDefault("page", null))
    //         .build();
    // }

    // private static TopHeadlinesEndpoint createTopHeadlinesEndpoint(HashMap<String, String> endpointDataHashMap)
    // {
    //     // Assigns a default value to category.
    //     if (endpointDataHashMap.get("category") == null)
    //     {
    //         endpointDataHashMap.put("category", "general");
    //     }

    //     return new TopHeadlinesEndpoint.Builder()
    //         .country(endpointDataHashMap.getOrDefault("country", null))
    //         .category(endpointDataHashMap.getOrDefault("category", "general"))
    //         .sources(endpointDataHashMap.getOrDefault("sources", null))
    //         .q(endpointDataHashMap.getOrDefault("q", null))
    //         .pageSize(endpointDataHashMap.getOrDefault("pageSize", null))
    //         .page(endpointDataHashMap.getOrDefault("page", null))
    //         .build();
    // }

    // private static SourcesEndpoint createSourcesEndpoint(HashMap<String, String> endpointDataHashMap)
    // {
    //     return new SourcesEndpoint.Builder()
    //         .category(endpointDataHashMap.getOrDefault("category", null))
    //         .language(endpointDataHashMap.getOrDefault("language", null))
    //         .country(endpointDataHashMap.getOrDefault("country", null))
    //         .build();
    // }
}
