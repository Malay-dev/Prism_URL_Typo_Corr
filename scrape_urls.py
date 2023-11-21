from bs4 import BeautifulSoup
import requests
import json
import os


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def create_gist(data, github_token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Get a list of gists
    response = requests.get("https://api.github.com/gists", headers=headers)
    gists = response.json()

    # Check if a Gist with the file name already exists
    existing_gist_id = None
    for gist in gists:
        if "scraped_data.json" in gist["files"]:
            existing_gist_id = gist["id"]
            break

    if existing_gist_id:
        # Update the existing Gist with new data
        gist_payload = {
            "files": {
                "scraped_data.json": {
                    "content": json.dumps(data, indent=2, ensure_ascii=False)
                }
            }
        }
        response = requests.patch(
            f"https://api.github.com/gists/{existing_gist_id}",
            headers=headers,
            json=gist_payload
        )
    else:
        # Create a new Gist
        gist_payload = {
            "description": "Scraped data",
            "public": True,
            "files": {
                "scraped_data.json": {
                    "content": json.dumps(data, indent=2, ensure_ascii=False)
                }
            }
        }
        response = requests.post(
            "https://api.github.com/gists",
            headers=headers,
            json=gist_payload
        )

    if response.status_code == 200 or response.status_code == 201:
        gist_url = response.json()["html_url"]
        return f"Gist created/updated: {gist_url}"
    else:
        return response.json()


def scraper(q: str, gl: str):
    params = {
        "q": q,    # query example
        "hl": "en",                         # language
        "gl": gl,                         # country of the search, UK -> United Kingdom
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
                "links": links,
                "location": gl
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

    create_gist(data=existing_data, github_token=GITHUB_TOKEN)
    return data
