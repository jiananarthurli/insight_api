from django.shortcuts import render
import requests
import json

# Create your views here.


def wikiExtractor(wikiTopic):

    url_base = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles='

    url = url_base + wikiTopic

    page_r = requests.get(url)
    page_content = page_r.content
    page_json = json.loads(page_content)

    pageId = list(page_json['query']['pages'].keys())[0]
    extract = page_json['query']['pages'][pageId]['extract']

    return extract
