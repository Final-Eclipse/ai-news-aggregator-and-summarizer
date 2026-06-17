package scraper.news.services.parsers;

import java.util.HashMap;
import java.util.Map;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class Parser 
{                                                                       // https://stackoverflow.com/questions/15844035/best-hashmap-initial-capacity-while-indexing-a-list
    private static Map<String, String> newsOutlets = new HashMap<>()   // Change this number to match the number of keys in the HashMap. It helps performance. 
    {{
        put("abcnews.com", "div.xvlfx.ZRifP.TKoO.eaKKC.EcdEg.bOdfO.qXhdi.NFNeu.UyHES");
        put("www.aljazeera.com", "div.wysiwyg.wysiwyg--all-content");
        put("arstechnica.com", "div.post-content.post-content-double");
        put("apnews.com", "div.RichTextStoryBody.RichTextBody");
        // put("www.axios.com", "div.col-1-13");    Not a static webpage, need to possibly use Selenium.
        put("bleacherreport.com", "div.MuiStack-root.css-9bmycx");
        // put("www.bloomberg.com", "") Not a static webpage, need to possibly use Selenium.
        put("www.breitbart.com", "div.entry-content");
        put("www.businessinsider.com", "section.post-body-content.post-story-body-content");
        // put("www.buzzfeed.com", "div.buzz--list.buzz--Books.subbuzzes-wrapper.subbuzzes--buzzfeed"); Error Code 406
    }};

    public static String parse(String url, String html)
    {
        String websiteName = getWebsiteName(url);
        String cssQuery = newsOutlets.get(websiteName);
        
        Document doc = Jsoup.parse(html, "UTF-8");
        String pageContent = doc.selectFirst(cssQuery).text();
        System.out.println(pageContent);
        return pageContent;
    }

    private static String getWebsiteName(String url)
    {
        int offset = 2;
        int x = url.indexOf("//") + offset;
        int y = url.substring(x).indexOf("/");

        if (y == -1)
        {
            y = url.length();
        }
        else
        {
            y += x;
        }

        String title = url.substring(x, y);
        return title;
    }
}
