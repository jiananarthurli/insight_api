from django.shortcuts import render
import requests
import json

# Create your views here.

# find the exact topic text for wiki API
def wiki_find_redirect(topic):
    url = 'https://en.wikipedia.org/w/api.php?action=query&titles=' + topic + '&&redirects&format=json'
    r = requests.get(url)
    pageid = list(json.loads(r.text)['query']['pages'].keys())[0]
    title = json.loads(r.text)['query']['pages'][pageid]['title']
    return title


# extract wiki text using wiki API
def wikiExtractor(wikiTopic):

    url_base = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles='

    title = wiki_find_redirect(wikiTopic)
    url = url_base + title

    page_r = requests.get(url)
    page_content = page_r.content
    page_json = json.loads(page_content)

    pageId = list(page_json['query']['pages'].keys())[0]
    extract = page_json['query']['pages'][pageId]['extract']

    return extract
