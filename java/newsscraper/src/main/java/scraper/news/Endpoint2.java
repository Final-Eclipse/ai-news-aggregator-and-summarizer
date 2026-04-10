package scraper.news;

// What does the parent Endpoint abstract class need?
// What does each child need specifically?

// Parent only needs apiKey as parameters are at most shared between 2 endpoints not all three.
// The apiKey is the only parameter needed by all three endpoints.
// The apikey is handled by the NewsScraper class though.
// Perhaps a parent class is not needed.

// Children need methods to get their request parameters.

// NewsAPI only allows 100 api requests per day.
abstract class Endpoint2
{
    protected String apiUrl;




}