package scraper.news.models.data_transfer_objects;

import scraper.news.models.value_objects.Article;

public class TopHeadlinesDto
{
    private String status;
    private int totalResults;
    private Article[] articles;

    // Getters
    public String getStatus() { return status; }
    public int getTotalResults() { return totalResults; }
    public Article[] getArticles() { return articles; }

    // Setters
    public void setStatus(String status) { this.status = status; }
    public void setTotalResults(int totalResults) { this.totalResults = totalResults; }
    public void setArticles(Article[] articles) { this.articles = articles; }
}
