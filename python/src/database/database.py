import sqlite3

def get_connection() -> sqlite3.Connection:
    """Return a sqlite3.Connecton object."""
    connection = sqlite3.connect("src/database/news_articles.db")
    return connection

def get_cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    """Return a sqlite3.Cursor object."""
    cursor = connection.cursor()
    return cursor

def create_table_everything() -> None:
    """Create a table in the database named everything."""
    connection = get_connection()
    cursor = get_cursor(connection)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS everything(
            id STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            name STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            author STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            title STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            description STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            url STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            urlToImage STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            publishedAt STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            content STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            PRIMARY KEY (id, name, author, title, description, url, urlToImage, publishedAt, content)
    )""")
    connection.close()

def _drop_table_everything() -> None:
    """Drops the everything table from the database if it exists."""
    connection = get_connection()
    cursor = get_cursor(connection)
    cursor.execute("""DROP TABLE IF EXISTS everything""")
    connection.close()

def add_to_table_everything(response: dict) -> None:
    """
    Adds each article object from the response into the database's everything table.

    @param response: Dictionary object converted from JSON receieved from News API.
    """
    connection = get_connection()
    cursor = get_cursor(connection)

    for article in response["articles"]:
        id = article["source"]["id"]
        name = article["source"]["name"]
        author = article["author"]
        title = article["title"]
        description = article["description"]
        url = article["url"]
        urlToImage = article["urlToImage"]
        publishedAt = article["publishedAt"]
        content = article["content"]

        data = (id, name, author, title, description, url, urlToImage, publishedAt, content)
        cursor.execute("INSERT OR REPLACE INTO everything VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

    connection.commit()
    connection.close()

def query_table_everything(bindings: dict) -> dict:
    connection = get_connection()
    cursor = get_cursor(connection)

    database_columns: list = ["id", "name", "author", "title", "description", "url", "urlToImage", "publishedAt", "content"]

    searchIn: str = bindings["searchIn"]
    if "Title" in searchIn:
        database_columns.remove("description")
        database_columns.remove("content")
    if "Description" in searchIn:
        database_columns.remove("title")
        database_columns.remove("content")
    if "Content" in searchIn:
        database_columns.remove("title")
        database_columns.remove("description")

    # For language, add all sources to the database first.
    # Then, when adding new articles, check its source and compare it with the one in the sources table and set its language to what is in the sources table.
    # Drop current everything table and make new one with language column or add new language column and replace its value for every article while also checking what language it is
    # based off of the sources table. 

    # Assemble queries.
    q: str = "(\n  " + " LIKE :q OR\n  ".join(database_columns) + " LIKE :q\n)"
    sources: str = "(\n  id LIKE :id AND\n  name LIKE :name\n)"
    domains: str = "(\n  url LIKE :domains\n)"
    # language: str # Use sources database table to determine, make sure sources table exists, if not, create one and populate it.
    
    if bindings["excludeDomains"] != "%%":
        excludeDomains: str = "(\n  url NOT LIKE :excludeDomains\n)"
    else:
        excludeDomains = ""

    if bindings["from"] != "" and bindings["to"] != "":
        time: str = "(\n  publishedAt > :from AND\n  publishedAt < :to\n)"
    else:
        time: str = ""

    queries = (q, sources, domains, excludeDomains, time)
    query = "\nAND\n".join([x for x in queries if x != ""]) # Adds each query as long as it is not an empty string (mainly for time query).

    # Execute query selection.
    results = cursor.execute(f"""SELECT * FROM everything WHERE {query}""", bindings).fetchall()
    
    connection.close()
    return results

def create_table_top_headlines() -> None:
    """Create a table in the database named top_headlines."""
    connection = get_connection()
    cursor = get_cursor(connection)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS top_headlines(
            id STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            name STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            author STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            title STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            description STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            url STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            urlToImage STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            publishedAt STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            content STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            PRIMARY KEY (id, name, author, title, description, url, urlToImage, publishedAt, content)
    )""")
    connection.close()

def _drop_table_top_headlines() -> None:
    """Drops the top_headlines table from the database if it exists."""
    connection = get_connection()
    cursor = get_cursor(connection)
    cursor.execute("""DROP TABLE IF EXISTS top_headlines""")
    connection.close()

def add_to_table_top_headlines(response: dict) -> None:
    """
    Adds each article object from the response into the database's top_headlines table.

    @param response: Dictionary object converted from JSON receieved from News API.
    """
    connection = get_connection()
    cursor = get_cursor(connection)

    for article in response["articles"]:
        id = article["source"]["id"]
        name = article["source"]["name"]
        author = article["author"]
        title = article["title"]
        description = article["description"]
        url = article["url"]
        urlToImage = article["url"]
        publishedAt = article["publishedAt"]
        content = article["content"]

        data = (id, name, author, title, description, url, urlToImage, publishedAt, content)
        cursor.execute("INSERT OR REPLACE INTO top_headlines VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

    connection.commit()
    connection.close()

def create_table_sources() -> None:
    """Create a table in the database named sources."""
    connection = get_connection()
    cursor = get_cursor(connection)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources(
            id STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            name STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            description STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            url STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            category STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            language STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            country STRING NOT NULL ON CONFLICT REPLACE DEFAULT 'N/A',
            PRIMARY KEY (id, name, description, url, category, language, country)
    )""")
    connection.close()

def _drop_table_sources() -> None:
    """Drops the sources table from the database if it exists."""
    connection = get_connection()
    cursor = get_cursor(connection)
    cursor.execute("""DROP TABLE IF EXISTS sources""")
    connection.close()

def add_to_table_sources(response: dict) -> None:
    """
    Adds each source object from the response into the database's sources table.

    @param response: Dictionary object converted from JSON receieved from News API.
    """
    connection = get_connection()
    cursor = get_cursor(connection)

    for source in response["sources"]:
        id = source["id"]
        name = source["name"]
        description = source["description"]
        url = source["url"]
        category = source["category"]
        language = source["language"]
        country = source["country"]

        data = (id, name, description, url, category, language, country)
        cursor.execute("INSERT OR REPLACE INTO sources VALUES(?, ?, ?, ?, ?, ?, ?)", data)

    connection.commit()
    connection.close()

def query_table_sources(bindings: dict) -> dict:
    connection = get_connection()
    cursor = get_cursor(connection)

    # Assemble queries.
    category: str = "(\n  category LIKE :category\n)"
    language: str = "(\n  language LIKE :language\n)"
    country: str = "(\n  country LIKE :country\n)"

    queries = (category, language, country)
    query = "\nAND\n".join(queries)

    # Execute query selection.
    results = cursor.execute(f"""SELECT * FROM sources WHERE {query}""", bindings).fetchall()

    connection.close()
    return results

if __name__ == "__main__":
    pass
    # query_table_everything()
    # connection = get_connection()
    # cursor = get_cursor(connection)
    # connection.close()