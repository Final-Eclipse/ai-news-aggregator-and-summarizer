from PyQt5 import QtCore
import requests, json, time

# Create a GUI to display the article titles that follow the descriptions the user has set.
# Send a GET request for all of the articles for the specified endpoint (have a dropdown to select which endpoint, which changes what input fields are available).
# User will type the article's URL which will send a POST request to Spring Boot to scrape the article's text and update an endpoint like "/article-text".
# When the summarize button is clicked, send a GET request to C#.
# C# will send a GET request to Spring Boot for the article text and send another request to a local model using OllamaSharp.
# Send a POST request back to Spring Boot at "/summary" with the article's summary.
# In Python, send a GET request to Spring Boot to retrieve the summary and display it.

# Create a C# REST API that handles summarization.
# POST requests return data so Python can make a POST request with the article url to Spring Boot and it will wait until the summary is returned.
# Does C# need to be asynchronous or can it be synchronous.

def send_post_request(endpoint_data):
    """Sends a POST request to upload endpoint data."""
    request = requests.post("http://localhost:8080/api/v1/news/post-endpoint-data", endpoint_data)
    print(request.text)

def send_summary(article_text):
    request = requests.post("http://localhost:8080/api/v1/news/summary", article_text)  # Article text should be in JSON format.
    print(request.text)

def create_everything():
    """Returns a JSON string."""
    query_params = {
        "endpoint": "everything",
        "q": "iran",
        "searchIn": "title",
        "sources": "associated-press",
        "domains": None,
        "excludeDomains": None,
        "from": get_oldest_date(),
        "to": get_current_date(),
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": "100",
        "page": "1" 
    }

    return json.dumps(query_params)

def create_top_headlines():
    """Returns a JSON string."""
    query_params = {
        "endpoint": "top-headlines",
        "country": "us",
        "category": None,
        "sources": None,
        "q": "trump",
        "pageSize": "100",
        "page": "1"
    }

    return json.dumps(query_params)

def create_sources():
    """Returns a JSON string."""
    query_params = {
        "endpoint": "top-headlines/sources",
        "category": "general",
        "language": "en",
        "country": "us"
    }

    return json.dumps(query_params)

def get_current_date():
    """Returns the current date."""
    local_time = time.localtime()
    year = time.strftime("%Y", local_time)
    month = time.strftime("%m", local_time)
    day = time.strftime("%d", local_time)
    date = f"{year}-{month}-{day}"

    return date

def get_oldest_date():
    "Returns a date for the furthest back the NewsAPI allows (one month back) in ISO 8601 format."
    current_date = get_current_date()
    month = int(current_date[5:7]) - 1
    year = int(current_date[0:4])
    day = int(current_date[8:]) + 1

    # Changes month to December and year to previous if needed.
    if month <= 0:
        month = 12
        year -= 1
    

    # Prefixes a 0 to the month and day if needed.
    if month < 10:
        month = f"0{month}"
    if day < 10:
        day = f"0{day}"

    oldest_date = f"{year}-{month}-{day}"
    return oldest_date

# send_post_request(create_everything())
# send_post_request(create_top_headlines())    
# send_post_request(create_sources())

send_summary("What is an interesting fact about something in history?")







    
