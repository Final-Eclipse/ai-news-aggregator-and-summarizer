using Microsoft.AspNetCore.Mvc;
using ai_news_aggregator_and_summarizer.Services;

namespace ai_news_aggregator_and_summarizer.Controllers;

[ApiController]
[Route("[controller]")]
public class SummaryController : ControllerBase
{
    // Return IActionResult, ActionResult, or IEnumerable?
    [HttpPost]
    public string PostArticleText([FromBody] string articleText)
    {
        return SummaryService.GetSummary(articleText).Result.summaryText;
    }
}