package scraper.news;

import java.util.HashMap;

public class CreateEndpoint 
{
    private void determineEndpoint(HashMap<String, String> endpointDataHashMap)
    {
        switch (endpointDataHashMap.get("endpoint"))
        {
            case "everything":
                break;
            case "top-headlines":
                break;
            case "top-headlines/sources":
                break;
            default:
                throw new IllegalArgumentException("Invalid endpoint type.");
        }
    }

    public Endpoint create(HashMap<String, String> endpointDataHashMap)
    {
        determineEndpoint(endpointDataHashMap);

        return new SourcesEndpoint.Builder()
            .category("sports")
            .language("en")
            .country("us")
            .build();
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
