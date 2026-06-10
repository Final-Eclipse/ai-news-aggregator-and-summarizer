package scraper.news.models.data_transfer_objects;

public class EndpointDto
{
    private String endpoint;

    // At least one is required.
    private String q;
    private String searchIn;  // Need to have logic to serialize into a list and separate commas, spaces, etc. (in EverythingEndpoint.java).
    private String sources;   // Can't be mixed with country or category parameters.
    private String domains;
    private String excludeDomains;
    private String country; // Can't be mixed with the sources parameter.
    private String category;    // Can't be mixed with the sources parameter.

    // Optional
    private String from;
    private String to;
    private String language;
    private String sortBy;
    private String pageSize;
    private String page;     

    // Getters
    public String getEndpoint() { return endpoint; }
    public String getQ() { return q; }
    public String getCountry() { return country; }
    public String getCategory() { return category; }
    public String getSearchIn() { return searchIn; }
    public String getSources() { return sources; }
    public String getDomains() { return domains; }
    public String getExcludeDomains() { return excludeDomains; }
    public String getFrom() { return from; }
    public String getTo() { return to; }
    public String getLanguage() { return language; }
    public String getSortBy() { return sortBy; }
    public String getPageSize() { return pageSize; }
    public String getPage() { return page; }

    // Setters
    public void setEndpoint(String endpoint) { this.endpoint = endpoint; }
    public void setQ(String q) { this.q = q; }
    public void setCountry(String country) { this.country = country; }
    public void setCategory(String category) { this.category = category; }
    public void setSearchIn(String searchIn) { this.searchIn = searchIn; }
    public void setSources(String sources) { this.sources = sources; }
    public void setDomains(String domains) { this.domains = domains; }
    public void setExcludeDomains(String excludeDomains) { this.excludeDomains = excludeDomains; }
    public void setFrom(String from) { this.from = from; }
    public void setTo(String to) { this.to = to; }
    public void setLanguage(String language) { this.language = language; }
    public void setSortBy(String sortBy) { this.sortBy = sortBy; }
    public void setPageSize(String pageSize) { this.pageSize = pageSize; }
    public void setPage(String page) { this.page = page; }
}

    
