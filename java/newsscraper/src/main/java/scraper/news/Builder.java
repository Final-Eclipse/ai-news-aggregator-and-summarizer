// package scraper.news;

// // Builder.
// public class Builder
// {
//     // private String apiURL;
//     // private String country;
//     // private String category;
//     // private String sources;
//     // private String keywords;

//     // public static class EverythingEndpoint
//     // {
//     //     private String q;
//     //     private String searchIn;
//     //     private String sources;
//     //     private String domains;
//     //     private String excludeDomains;
//     //     private String from;
//     //     private String to;
//     //     private String language;
//     //     private String sortBy;
//     //     private String pageSize;
//     //     private String page;

//     //     //apikey, q, searchIn, sources, domains, excludeDomains, from, to, language, sortBy, pageSize, page
//     // }

//     public static class TopHeadlinesEndpoint
//     {
//         private String country;
//         private String category;
//         private String sources;
//         private String q;
//         private String pageSize;
//         private String page;
        
//         // apikey, country, category, sources, q, pageSize, page
//     }

//     public static class SourcesEndpoint
//     {
//         private String category;
//         private String language;
//         private String country;

//         // apikey, category, language, country
//     }

//     public Builder setApiURL(String apiURL)
//     {
//         this.apiURL = apiURL;
//         return this;
//     }

//     // The 2-letter ISO 3166-1 code of the country you want to get headlines for. 
//     // Possible options: us. 
//     // Note: you can't mix this param with the sources param.
//     public Builder setCountry(String country)
//     {
//         this.country = country;
//         return this;
//     }

//     // Find sources that display news of this category. 
//     // Possible options: business, entertainment, general, health, science, sports, technology. Default: all categories.
//     public Builder setCategory(String category)
//     {
//             this.category = category;
//             return this;
//     }

//     // A comma-seperated string of identifiers for the news sources or blogs you want headlines from. 
//     // Use the /top-headlines/sources endpoint to locate these programmatically or look at the sources index. 
//     // Note: you can't mix this param with the country or category params.
//     public Builder setSource(String... sources)
//     {
//         // this.sources = sources;
//         return this;
//     }

//     // Keywords or a phrase to search for.
//     public Builder setKeywords(String keywords)
//     {
//         // Splits the keywords (ex. Trump and Epstein) and inserts a + in place of each space (Trump+and+Epstein).
//         String[] splitKeywords = keywords.split(" ");
        
//         for (String x : splitKeywords)
//         {
//             this.keywords = x + "+";
//         }

//         int index = this.keywords.lastIndexOf("+");
//         this.keywords = this.keywords.substring(0, index);
//         return this;
//     }

//     public NewsScraper buildNewsScraper()
//     {
//         return new NewsScraper(this);
//     }  

//     public Builder()
//     {
//         this.apiURL = builder.apiURL;
//         this.country = builder.country;
//         this.category = builder.category;
//     }

//     private NewsScraper(Builder builder)
//     {
//         this.apiURL = builder.apiURL;
//         this.country = builder.country;
//         this.category = builder.category;

//         return new NewsScraper();
//     }
// }