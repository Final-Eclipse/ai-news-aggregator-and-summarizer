package scraper.news;

import java.io.IOException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;

import scraper.news.services.HttpService;
import scraper.news.services.parsers.Parser;

@SpringBootApplication
public class Main 
{
    public static void main(String[] args) throws IOException
    {
        // mvn spring-boot:run
        // or
        // .\/mvnw.cmd spring-boot:run
        // To run from terminal, use "mvn spring-boot:run" in the newsscraper directory.
        // Spring Boot
        SpringApplication.run(Main.class, args);

        // HttpService.getWebsiteResponse("https://www.buzzfeed.com/kristenharris1/tell-us-about-the-worst-celebrity-memoir-youve-ever-read?origin=web-hf");

        // ApNewsParser x = new ApNewsParser("<html><head><title>First parse</title></head>");
        // ApNewsParser x = new ApNewsParser("https://apnews.com/article/g7-iran-ukraine-trump-macron-zelenskyy-e7fad4eabaae8181f70fa5a0b9e499b2");

        // System.out.println(summarize("https://www.axios.com/2026/06/16/anthropic-fable-trump-white-house-cybersecurity"));
    }

    // public static String summarize(String url) 
    // {     
    //     String websiteHtml = getWebsiteHtml(url);
    //     String pageContent = Parser.parse(url, websiteHtml);
    //     String summary = HttpService.getSummarization(pageContent);
    //     return summary;
    // }

    // private static String getWebsiteHtml(String url)
    // {
    //     return HttpService.getWebsiteResponse(url);
    // }
}