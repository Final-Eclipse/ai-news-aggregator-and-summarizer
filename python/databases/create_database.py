import sqlite3
from sqlite3 import Connection, Cursor

def get_connection_and_cursor() -> tuple:
    connection = sqlite3.connect("databases/news.db")
    cursor = connection.cursor()
    return connection, cursor

def create_everything():
    connection, cursor = get_connection_and_cursor()
    connection : Connection
    cursor: Cursor

    cursor.execute("""DROP TABLE IF EXISTS everything""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS everything(
            primary_key INTEGER PRIMARY KEY, 
            id STRING,
            name STRING, 
            author STRING, 
            title STRING,
            description STRING,
            url STRING,
            urlToImage STRING,  
            publishedAT STRING,
            content STRING
    )""")

def get_everything_data() -> tuple:
    # articles = []

    # with open(file/path, "w") as file:
        # for article in everything.json file:
        #     Create tuple and populate with values
        #     Add tuple to list
    
    # return list

    # Extract these two values from source key
    id = "associated-press"
    name = "Associated Press"

    author = "AP"
    title = "Trump Administration Asked National Park Visitors To Report “Negative” History Info. Visitors Did Something Different."
    description = "The Trump administration recently asked visitors to U.S. national parks to report displays or exhibits saying “negative” things about Americans and to restore sites as “uplifting public monuments.\" But a large chunk of the 35,000 people who responded instead …"
    url = "https://apnews.com/article/national-park-service-doug-burgum-donald-trump-c58eb3278c9ce787afacf37f6845ff4c"
    urlToImage = "https://dims.apnews.com/dims4/default/7af89c8/2147483647/strip/true/crop/5048x3364+0+1/resize/980x653!/quality/90/?url=https%3A%2F%2Fassets.apnews.com%2Ff4%2Ff3%2F659d9e3f601ca643b5c07b9142e0%2F51bbebdb10f74e82bea3dbf556b64607"
    publishedAt = "2026-06-10T14:04:00Z"
    content = "BISMARCK, N.D. (AP) The Trump administration last year issued a plea to visitors at U.S. national parks: Report any displays or exhibits saying negative things about Americans living in the past or p… [+5837 chars]"

    data = (None, id, name, author, title, description, url, urlToImage, publishedAt, content)

    return data

def add_to_everything() -> None:
    connection, cursor = get_connection_and_cursor()
    connection: Connection
    cursor: Cursor

    cursor.execute("""INSERT INTO everything VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", get_everything_data())

    print(cursor.execute("SELECT * FROM everything").fetchall())
    # print(cursor.execute("SELECT rowID FROM everything").fetchall())

    connection.commit()

# create_everything()
add_to_everything()