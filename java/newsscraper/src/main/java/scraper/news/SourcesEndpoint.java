package scraper.news;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class SourcesEndpoint extends Endpoint
{
    private String baseApiEndpointUrl = "https://newsapi.org/v2/top-headlines/sources";
    private String category;
    private String language;
    private String country;    

    public SourcesEndpoint(Builder builder)
    {
        this.category = builder.category;
        this.language = builder.language;
        this.country = builder.country;

        setApiEndpointUrl(baseApiEndpointUrl);
        addParametersToHashMap();
        appendQueryParameters();
    }

    public void addParametersToHashMap()
    {
        HashMap<String, Object> parametersHashMap = getParametersHashMap();

        parametersHashMap.put("category", category);
        parametersHashMap.put("language", language);
        parametersHashMap.put("country", country);

        setParametersHashMap(parametersHashMap);
    }

    public static class Builder
    {
        private String category;   
        private String language; 
        private String country; 

        public Builder()
        {
            
        }
        
        // Required, at least one.
        public Builder category(String category) { this.category = category; return this; }
        public Builder language(String language) { this.language = language; return this; }
        public Builder country(String country) { this.country = country; return this; }
        
        public SourcesEndpoint build()
        {
            if (category == null && language == null && country == null)
            {
                throw new NullPointerException("At least one of these parameters must not be null (category, language, country).");
            }
            
            return new SourcesEndpoint(this);
        }
    }
}
