import requests
from django.core.cache import cache

def cache_product_data(urls):
    """
    Caches product data from the given list of URLs.

    Args:
        urls (list): List of URLs from which to fetch product data.

    Returns:
        None
    """
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "contents" in data and data["contents"]:
                    content = data["contents"][0]
                    if "mainContent" in content and content["mainContent"]:
                        main_content = content["mainContent"][0]
                        if "contents" in main_content and main_content["contents"]:
                            records = main_content["contents"][0]["records"]
                            cache.set(url, records)
        except Exception as e:
            print(f"Error caching data from {url}: {e}")