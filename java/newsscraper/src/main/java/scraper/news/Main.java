package scraper.news;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Main 
{
    public static void main(String[] args) 
    {
        // mvn spring-boot:run
        // or
        // .\/mvnw.cmd spring-boot:run
        // To run from terminal, use "mvn spring-boot:run" in the newsscraper directory.
        // Spring Boot
        SpringApplication.run(Main.class, args);
    }
}