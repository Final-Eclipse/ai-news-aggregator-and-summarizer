package scraper.news.models.data_transfer_objects;

import scraper.news.models.value_objects.Source;

public class SourcesDto
{
    private String status;
    private Source[] sources;

    // Getters
    public String getStatus()
    {
        return status;
    }
    
    public Source[] getSources()
    {
        return sources;
    }

    // Setters
    public void setStatus(String status)
    {
        this.status = status;
    }

    public void setSources(Source[] sources)
    {
        this.sources = sources;
    }
}
