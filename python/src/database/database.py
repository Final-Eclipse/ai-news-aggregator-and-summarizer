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
        urlToImage = article["url"]
        publishedAt = article["publishedAt"]
        content = article["content"]

        data = (id, name, author, title, description, url, urlToImage, publishedAt, content)
        cursor.execute("INSERT OR REPLACE INTO everything VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", data)

    connection.commit()
    connection.close()

def query_table_everything(bindings: dict) -> dict:
    connection = get_connection()
    cursor = get_cursor(connection)

    # Get database columns
    database_columns: list = []
    database_column_info: list = cursor.execute("""PRAGMA table_info(everything)""").fetchall()
    for column_info in database_column_info:
        database_columns.append(column_info[1])

    # Assemble queries.
    q: str = "(\n  " + " LIKE :q OR\n  ".join(database_columns) + " LIKE :q\n)"
    sources: str = "(\n  id LIKE :id AND\n  name LIKE :name\n)"
    domains: str = "(\n  url LIKE :domains\n)"

    if bindings["from"] != "" and bindings["to"] != "":
        time: str = "(\n  publishedAt > :from AND\n  publishedAt < :to\n)"
    else:
        time: str = ""

    queries = (q, sources, domains, time)
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

def query_table_top_headlines(bindings: dict) -> dict:
    connection = get_connection()
    cursor = get_cursor(connection)

    # Get database columns
    database_columns: list = []
    database_column_info: list = cursor.execute("""PRAGMA table_info(top_headlines)""").fetchall()
    for column_info in database_column_info:
        database_columns.append(column_info[1])

    # Assemble queries.
    q: str = "(\n  " + " LIKE :q OR\n  ".join(database_columns) + " LIKE :q\n)"
    sources: str = "(\n  id LIKE :id AND\n  name LIKE :name\n)"
    # category: str = "(\n  category LIKE :category\n)" 
    # country: str = "(\n  country LIKE :country\n)"

    queries = (q, sources)
    # queries = (q, sources, category, country)
    query = "\nAND\n".join((q, sources))

    # Execute query selection.
    results = cursor.execute(f"""SELECT * FROM top_headlines WHERE {query}""", bindings).fetchall()

    connection.close()
    return results

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

if __name__ == "__main__":
    # query_table_everything()
    connection = get_connection()
    cursor = get_cursor(connection)

    columns = cursor.execute("""PRAGMA table_info(everything)""").fetchall()
    print(*columns)
    # for column in columns:
    #     print(column[1])

    connection.close()