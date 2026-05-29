using Microsoft.AspNetCore.Mvc;
using ai_news_aggregator_and_summarizer.Services;

namespace ai_news_aggregator_and_summarizer.Controllers;

[ApiController]
[Route("[controller]")]
public class SummaryController : ControllerBase
{
    // public SummaryController()
    // {
    
    // }

    public string GetSummary(string articleText)
    {
        return SummaryService.Get(articleText).Result.summaryText;
    }
    
    // GET by Id action

    // POST action

    // PUT action

    // DELETE action
}