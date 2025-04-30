import requests


def fetch_wikipedia_link(movie_title: str) -> str:
    """
    Query the Wikipedia API to find the page link for the given movie_title.
    Returns a URL string, or None if an error occurs or no page found.
    """
    try:
        # We can search for the exact movie title
        base_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": movie_title,
            "format": "json",
        }
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()

        # Identify the pageid from the search results
        search_results = data.get("query", {}).get("search", [])
        if not search_results:
            return None

        pageid = search_results[0]["pageid"]
        return f"https://en.wikipedia.org/?curid={pageid}"
    except requests.RequestException:
        return None
