from PyQt5 import QtCore
import requests, json

# Create a GUI to display the article titles that follow the descriptions the user has set.
# Send a GET request for all of the articles for the specified endpoint (have a dropdown to select which endpoint, which changes what input fields are available).
# User will type the article's URL which will send a POST request to Spring Boot to scrape the article's text and update an endpoint like "/article-text".
# When the summarize button is clicked, send a GET request to C#.
# C# will send a GET request to Spring Boot for the article text and send another request to a local model using OllamaSharp.
# Send a POST request back to Spring Boot at "/summary" with the article's summary.
# In Python, send a GET request to Spring Boot to retrieve the summary and display it.

def send_post_request(endpoint_data):
    """Sends a POST request to upload endpoint data."""
    requests.post("http://localhost:8080/api/v1/news/post-endpoint-data", endpoint_data)

def create_top_headlines():
    """Returns a JSON string."""
    query_params = {
        "endpoint": "everything",
        "q": "iran",
        "searchIn": "title",
        "sources": "associated-press",
        "domains": "null",
        "excludeDomains": "null",
        "from": "2026-05-01",
        "to": "2026-05-22",
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": "100",
        "page": "1" 
    }

    return json.dumps(query_params)

send_post_request(create_top_headlines())    


    
