import requests
import os

def search_cache(query):
    print(query)
    print("Searching for cached movies on remote server")
    if query['type'] == "movie":
        url = os.environ.get('CACHE_URL') + "/getResult/movie/"
        response = requests.get(url, json=query)
        return response.json()
    if query['type'] == "series":
        url = os.environ.get('CACHE_URL') + "/getResult/series/"
        response = requests.get(url, json=query)
        return response.json()
