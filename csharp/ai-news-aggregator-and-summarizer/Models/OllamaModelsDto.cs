using ai_news_aggregator_and_summarizer.Services;

namespace ai_news_aggregator_and_summarizer.Models;

public class OllamaModelsDto
{
    private List<string>? localModels = SummaryService.ListLocalModels();

    public List<string>? LocalModels
    {
        get { return localModels; }
        set { localModels = value; }
    }
}