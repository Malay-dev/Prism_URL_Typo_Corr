import fuzzywuzzy
from fuzzywuzzy import fuzz


def get_fuzzy_results(data, url):
    url_array = []
    for obj in data:
        link = obj["links"]
        ratio = fuzz.ratio(url, link)        
        url_array.append({"url": link, "ratio": ratio})
    sorted_url_array = sorted(
        url_array, key=lambda x: x['ratio'], reverse=True)
    return sorted_url_array
