from PyQt5 import QtCore

# Create a GUI to display the article titles that follow the descriptions the user has set.
# Send a GET request for all of the articles for the specified endpoint.
# User will type the article's URL which will send a POST request to Spring Boot to scrape the article's text and update an endpoint like "/article-text".
# When the summarize button is clicked, send a GET request to C#.
# C# will send a GET request to Spring Boot for the article text and send another request to a local model using OllamaSharp.
# Send a POST request back to Spring Boot at "/summary" with the article's summary.
# In Python, send a GET request to Spring Boot to retrieve the summary and display it.