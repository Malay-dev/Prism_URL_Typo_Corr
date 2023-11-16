from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import json
import os

params = {
    "api_key": "...",                  # serpapi key, https://serpapi.com/manage-api-key
    "engine": "google",                # serpapi parser engine
    "q": "How to change a car tire",   # search query
    "gl": "uk",                        # country of the search, UK -> United Kingdom
    # number of results per page (100 per page in this case)
    "num": "100"
    # other search parameters: https://serpapi.com/search-api#api-parameters
}

search = GoogleSearch(params)      # where data extraction happens

organic_results_data = []
page_num = 0

while True:
    results = search.get_dict()    # JSON -> Python dictionary

    page_num += 1

    for result in results["organic_results"]:
        organic_results_data.append({
            "title": result.get("title"),
            "snippet": result.get("snippet"),
            "link": result.get("link")
        })

    if "next_link" in results.get("serpapi_pagination", []):
        search.params_dict.update(dict(
            parse_qsl(urlsplit(results.get("serpapi_pagination").get("next_link")).query)))
    else:
        break

print(json.dumps(organic_results_data, indent=2, ensure_ascii=False))
