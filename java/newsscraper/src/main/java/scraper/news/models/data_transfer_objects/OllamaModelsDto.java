package scraper.news.models.data_transfer_objects;

import java.util.List;

public class OllamaModelsDto 
{
    private List<String> localModels;    

    public List<String> getLocalModels()
    {
        return localModels;
    }

    public void setLocalModels(List<String> localModels)
    {
        this.localModels = localModels;
    }
}
