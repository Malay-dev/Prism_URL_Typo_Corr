from bs4 import BeautifulSoup
import requests
import json
import lxml


def scraper(q: str):
    params = {
        "q": q,    # query example
        "hl": "en",                         # language
        # "gl": "uk",                         # country of the search, UK -> United Kingdom
        "start": 0,                         # number page by default up to 0
        # parameter defines the maximum number of results to return.
        "num": 100
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    page_num = 0

    data = []

    while True:
        page_num += 1
        html = requests.get("https://www.google.com/search",
                            params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, 'lxml')

        for result in soup.select(".tF2Cxc"):
            title = result.select_one(".DKV0Md").text
            try:
                snippet = result.select_one(".lEBKkf span").text
            except:
                snippet = None
            links = result.select_one(".yuRUbf a")["href"]

            data.append({
                "title": title,
                "snippet": snippet,
                "links": links
            })

        if soup.select_one(".d6cvqb a[id=pnnext]"):
            params["start"] += 1
        else:
            break
    try:
        with open("results.json", "r", encoding="utf-8") as file_obj:
            existing_data = json.load(file_obj)
    except FileNotFoundError:
        existing_data = []

    # Append the new data to the existing dataset
    existing_data.extend(data)
    # Write the combined dataset back to the file
    with open("results.json", "w", encoding="utf-8") as file_obj:
        json.dump(existing_data, file_obj, indent=2, ensure_ascii=False)
    return data
