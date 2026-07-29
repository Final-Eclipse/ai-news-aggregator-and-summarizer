class Domains():
    domains = (
        "abcnews.go.com",
        "www.aljazeera.com",
        "arstechnica.com",
        "apnews.com",
        "www.axios.com",
        "www.bleacherreport.com",
        "www.bloomberg.com",
        "www.breitbart.com",
        "www.businessinsider.com",
        "www.buzzfeed.com",
        "www.cbsnews.com",
        "us.cnn.com",
        "cnnespanol.cnn.com",
        "www.ccn.com",
        "www.engadget.com",
        "www.espn.com",
        "www.espncricinfo.com",
        "fortune.com",
        "www.foxnews.com",
        "www.foxsports.com",
        "news.google.com",
        "news.ycombinator.com",
        "www.ign.com",
        "mashable.com",
        "www.medicalnewstoday.com",
        "www.ms.now",
        "www.mtv.com/news",
        "news.nationalgeographic.com",
        "www.nationalreview.com",
        "www.nbcnews.com",
        "www.newscientist.com/section/news",
        "www.newsweek.com",
        "nymag.com",
        "www.nextbigfuture.com",
        "www.nfl.com",
        "www.nhl.com/news",
        "www.politico.com",
        "www.polygon.com",
        "www.recode.net",
        "www.reddit.com/r/all",
        "techcrunch.com",
        "www.techradar.com",
        "www.theamericanconservative.com",
        "thehill.com",
        "www.huffingtonpost.com",
        "thenextweb.com",
        "www.theverge.com",
        "www.wsj.com",
        "www.washingtonpost.com",
        "www.washingtontimes.com",
        "time.com",
        "www.usatoday.com/news",
        "news.vice.com",
        "www.wired.com"
    )

    qcombobox_options = ["Select domain(s)"] + [domain for domain in domains]

if __name__ == "__main__":
    import requests, json

    request = requests.get("https://newsapi.org/v2/top-headlines/sources?country=us&apiKey=")
    response = json.loads(request.text)

    urls = []
    for source in response["sources"]:
        url: str = source["name"]

        url = url.replace("http://", "")
        url = url.replace("https://", "")

        if url[len(url) - 1] == "/":
            url = url.replace("/", "") 
        elif url[len(url) - 1] == "\\":
            url = url.replace("\\", "") 

        urls.append(f"\"{url}\"")

    print(",\n".join(urls))