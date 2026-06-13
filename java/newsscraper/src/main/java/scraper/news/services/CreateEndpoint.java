package scraper.news.services;

import scraper.news.models.data_transfer_objects.EndpointDto;
import scraper.news.services.newsapi_endpoints.EverythingEndpoint;
import scraper.news.services.newsapi_endpoints.SourcesEndpoint;
import scraper.news.services.newsapi_endpoints.TopHeadlinesEndpoint;

public class CreateEndpoint 
{
    /**
     * Determines the endpoint type, calls its creation method, and returns the EndpointService result.
     * 
     * @param endpointData EndpointDto that contains data describing the endpoint and its query parameters.
     * @return EndpointService, an abstract class containing the apiEndpointUrl and related methods. 
     */
    public static EndpointService create(EndpointDto endpointData)
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

    /**
     * Constructs and returns an EverythingEndpoint.
     * 
     * @param endpointData EndpointDto that contains data describing the endpoint and its query parameters.
     * @return EverythingEndpoint, a class that extends EndpointService.
     */
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

    /**
     * Constructs and returns a TopHeadlinesEndpoint.
     * 
     * @param endpointData EndpointDto that contains data describing the endpoint and its query parameters.
     * @return TopHeadlinesEndpoint, a class that extends EndpointService.
     */
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

    /**
     * Constructs and returns a SourcesEndpoint.
     * 
     * @param endpointData EndpointDto that contains data describing the endpoint and its query parameters.
     * @return SourcesEndpoint, a class that extends EndpointService.
     */
    private static SourcesEndpoint createSourcesEndpoint(EndpointDto endpointData)
    {
        return new SourcesEndpoint.Builder()
            .category(endpointData.getCategory())
            .language(endpointData.getLanguage())
            .country(endpointData.getCountry())
            .build();
    }
}
