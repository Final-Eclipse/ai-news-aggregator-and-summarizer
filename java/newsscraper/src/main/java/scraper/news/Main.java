package scraper.news;

import java.io.IOException;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import scraper.news.services.HttpService;

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
        SpringApplication.run(Main.class, args);    // Implement Swagger API docs?
        HttpService.setApiKey(HttpService.getApiKey());
    }
}