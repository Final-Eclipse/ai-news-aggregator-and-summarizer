using Microsoft.AspNetCore.Mvc;

namespace ai_news_aggregator_and_summarizer;

[ApiController]
[Route("[controller]")]
public class SummaryController : ControllerBase
{
    // public SummaryController()
    // {
    
    // }

    public String GetSummary()
    {
        return "This is a summary of a relevant and topical news article.";
    }
    
    // GET by Id action

    // POST action

    // PUT action

    // DELETE action
}