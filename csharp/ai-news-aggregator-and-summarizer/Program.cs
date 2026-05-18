namespace ai_news_aggregator_and_summarizer;

using OllamaSharp;
// https://github.com/awaescher/OllamaSharp/tree/main

public class Program
{   
    public static async Task Main(string[] args)
    {
        GlobalHttpClient httpClient = new GlobalHttpClient();
        
        // RestApiClient restApiClient = new RestApiClient(GlobalHttpClient.httpClient);
        // restApiClient.PrintResponse();
        string articleText = $@"Trump says he would support suspending the federal gas tax
Suspending the tax would require congressional approval, and it could cost the government billions of dollars in revenue.

Listen to this article with a free account

00:00
03:24


1x

A sign displays fuel prices at a Mobil gas station
Energy Secretary Chris Wright said Sunday that President Donald Trump was “open to all ideas” to cut the cost of gas.Ariana Drehsler / Bloomberg via Getty Images

Share
Add NBC News to Google

Savewith a NBCUniversal Profile
May 11, 2026, 1:05 PM EDT / Updated May 11, 2026, 6:09 PM EDT
By Megan Lebowitz
President Donald Trump told reporters Monday that he would support suspending the federal gas tax “until it’s appropriate.”

NBC News Icon
Subscribe to read this story ad-free

Get unlimited access to ad-free articles and exclusive content.

arrow
Suspending the tax, which is at about 18 cents per gallon, would require congressional approval.

Asked by a reporter whether he would suspend the tax, Trump said, “Yeah.”

“I’m going to reduce until the — let me tell you, as soon as this is over with Iran, as soon as it’s over, you’re going to see gasoline and oil drop like a rock,” he said.

Asked how long he would suspend the tax for, Trump said, “Until it’s appropriate.”

“It’s a small percentage, but it’s still money,” he added.

Trump says ceasefire with Iran is 'on massive life support'
03:30
Earlier Monday, Trump told CBS News in a phone interview that he thought suspending the tax was “a great idea.”

“We’re going to take off the gas tax for a period of time, and when gas goes down, we’ll let it phase back in,” he said.

Energy Secretary Chris Wright said in an interview Sunday on NBC News’ “Meet the Press” that Trump was “open to all ideas” to cut the cost of gas, including possibly pausing the federal gas tax.

Democrats introduced legislation in March to suspend the tax until October, but their proposal has stalled. Sen. Josh Hawley, R-Mo., introduced a similar bill Monday.

Hawley’s measure would suspend the 18.4 cents-per-gallon federal tax on gasoline and the 24.4 cents-per-gallon federal tax on diesel fuel for 90 days after enactment. It would also give the president the authority to extend the suspensions for 90 more days if he determined it was needed.

Recommended

Trump administration
Trump allies and Christian leaders kick off America’s 250th birthday with religious rally on National Mall

Trump administration
Senate parliamentarian rejects Trump’s ballroom fund in budget bill
“American workers and families deserve immediate relief and this legislation will do just that,” Hawley said in a statement.

Rep. Anna Paulina Luna, R-Fla., said Monday on X that she would introduce a bill “to suspend the federal gas tax in light of Trump’s recent remarks.” It was not immediately clear whether or how their legislation would differ from what Democrats proposed in March.

“American families need this relief on gas prices,” Luna wrote. “My office will be working directly with President Trump to ensure we deliver this win for the American people.”

Rep. Chris Pappas, D-N.H., and Sen. Mark Kelly, D-Ariz., led the March bill. Pappas responded to Trump’s support for suspending the gas tax by saying on X, “This should have happened months ago.”

“Let’s pass it this week,” he said in the post.

The federal gas tax helps fund the Highway Trust Fund, which supports highway and mass transit programs, according to the Tax Policy Center at the Brookings Institution. Suspending the tax for five months could ultimately cost the government billions in revenue used for the fund this fiscal year, according to the Bipartisan Policy Center, a Washington think tank.

But even if the federal gas tax were suspended, gas prices would not be likely to decrease by the full 18 cents per gallon. The Bipartisan Policy Center estimated that gas would most likely fall by 10 to 16 cents per gallon for consumers, while gasoline suppliers would get the rest of the benefit.

Gas prices have risen more than 50% since the start of the war in Iran. On Monday, the national gas price average was $4.52 per gallon.";

        LocalModelClient localModelClient = new LocalModelClient(GlobalHttpClient.httpClient);
        await localModelClient.SendMessage($"Can you summarize this article. \n{articleText}");
        Console.Write(localModelClient.GetResponse());


        // RestApiClient.PrintResponse();
        
        // Start localhost then run this.
        // Refresh localhost to show posted data.

    
        // HttpContent httpContent = new StringContent("testing if this will post", System.Text.Encoding.UTF8, "text/plain");
        // var content = new StringContent($"Summary of article: President Donald Trump has expressed support for suspending the federal gas tax. The tax is currently at 18 cents per gallon and would require congressional approval to be suspended. Republicans in Congress have introduced legislation to suspend the tax for 90 days or more, while Democrats introduced a similar bill in March but it has stalled. Suspending the tax could cost the government billions of dollars in revenue used for highway and mass transit programs. Gas prices have risen over 50% since the start of the war in Iran, with the national average currently at $4.52 per gallon.", System.Text.Encoding.UTF8, "text/plain");
        // await RestApiClient.PostSummarization("api/v1/news/summary", content);  
    }
}
