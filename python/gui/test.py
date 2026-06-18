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

def send_article_text_to_summarize(article_text):
    """Sends a POST request to upload endpoint data."""
    headers = {"Content-Type": "application/json"}

    request = requests.post("http://localhost:8080/api/v1/news/summary", data=article_text, headers=headers)
    # request = requests.post("http://localhost:5172/summary", data=endpoint_data, headers=headers)
    print(request.text)

def send_endpoint_data(endpoint_data):
    headers = {"Content-Type": "application/json"}
    request = requests.post("http://localhost:8080/api/v1/news/post-endpoint-data", data=endpoint_data, headers=headers)
    print(request.text)

def set_selected_model(model):
    """Updates the selected ollama model."""
    headers = {
        "Content-Type": "application/json"
    }
    request = requests.post("http://localhost:5172/SelectedModel", data=model)
    print(request.text)

def send_summary(article_text):
    request = requests.post("http://localhost:8080/api/v1/news/summary", article_text)  # Article text should be in JSON format.
    print(request.text)

def create_everything():
    """Returns a JSON string."""
    query_params = {
        "endpoint": "everything",
        "q": "trump",
        "searchIn": None,
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

# send_summary("What is an interesting fact about something in history?")

def create_summary():
    query_params = {
        "articleText": "Who is the most famous person currently?"
    }

    return json.dumps(query_params)

def create_selected_model():
    query_params = {
        "selectedModel": "huihui_ai/deepseek-r1-abliterated:8b"
    }

    return json.dumps(query_params)

send_endpoint_data(create_everything())
# send_endpoint_data(create_top_headlines())    
# send_endpoint_data(create_sources())
# print(requests.get("http://localhost:8080/api/v1/news/everything").text) # Must POST endpoint data first then send GET the endpoint response.
data = json.loads(requests.get("http://localhost:8080/api/v1/news/everything").text)
print(data["articles"][0]["title"])

# set_selected_model("huihui_ai/deepseek-r1-abliterated:8b")
# send_article_text_to_summarize(create_summary())
# send_post_request(json.dumps("hello how are you doing"))

# Send async calls eventually to prevent code execution blocking.
# Don't do json.dumps then pass that in a request as json= because then it would be double serializing the json which doesn't work.

# Host news app on localhost so it can be used across devices on the same network as well as its own standalone app executable.

import unidecode
from pathlib import Path
# x = requests.get("https://www.buzzfeed.com/kristenharris1/tell-us-about-the-worst-celebrity-memoir-youve-ever-read?origin=web-hf").text
# x = unidecode.unidecode(x)
# with open(f"{Path.cwd()}/gui/apnews_content.html", "w") as file:
#     file.write(x)

# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.nbcnews.com/news/us-news/deal-reached-united-states-iran-war-rcna350039").text)
# https://www.textise.net
# https://www.reddit.com/r/firefox/comments/pphbvg/how_can_i_make_a_webpage_load_only_links_and_text/
# https://search.brave.com/search?q=is+there+a+website+that+i+can+give+a+link+and+it+will+just+show+only+the+text&summary=1&conversation=093501258e7e076996f2e25de3d370045a4a
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.textise.net/showText.aspx?strURL=https%253A//apnews.com/article/trump-80th-birthday-ufc-biden-e14d1bbccc1cbaaad42fd541b1fe833d").text)
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://apnews.com/article/trump-80th-birthday-ufc-biden-e14d1bbccc1cbaaad42fd541b1fe833d").text)
# print(requests.get("https://apnews.com/article/trump-80th-birthday-ufc-biden-e14d1bbccc1cbaaad42fd541b1fe833d").text)

# print(requests.get("https://www.textise.net/showText.aspx?strURL=https%253A//apnews.com/article/trump-80th-birthday-ufc-biden-e14d1bbccc1cbaaad42fd541b1fe833d").text)

# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://abcnews.com/US/child-killed-after-officer-fires-car-reported-shoplifting/story?id=133891802").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.aljazeera.com/news/2026/6/16/g7-leaders-meet-in-france-with-iran-and-ukraine-high-on-agenda").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://arstechnica.com/gadgets/2026/06/20-years-of-intel-macs-why-apple-switched-and-why-it-switched-again/").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://apnews.com/article/g7-iran-ukraine-trump-macron-zelenskyy-e7fad4eabaae8181f70fa5a0b9e499b2").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.axios.com/2026/06/16/anthropic-fable-trump-white-house-cybersecurity").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://bleacherreport.com/articles/25441589-watch-lionel-messi-score-historic-hat-trick-argentina-video-2026-fifa-world-cup-opener").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.bloomberg.com/news/articles/2026-06-17/iran-to-gain-major-financial-relief-under-interim-deal-with-us?srnd=homepage-americas").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.breitbart.com/politics/2026/06/16/senate-shoots-down-resolution-to-limit-trumps-military-authority-over-iran/").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.businessinsider.com/spacex-cursor-spcx-stock-bill-ackman-elon-musk-ai-stocks-2026-6").text, end="\n\n")
# print(requests.post("http://localhost:8080/api/v1/news/summary", data="https://www.buzzfeed.com/kristenharris1/tell-us-about-the-worst-celebrity-memoir-youve-ever-read?origin=web-hf").text, end="\n\n")

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }
# print(requests.get("https://www.buzzfeed.com/kristenharris1/tell-us-about-the-worst-celebrity-memoir-youve-ever-read?origin=web-hf").text)
