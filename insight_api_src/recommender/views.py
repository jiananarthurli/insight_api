from django.shortcuts import render
from django.http import HttpResponse
from extractor.views import wikiExtractor
from vectorizer.views import article2Vec
import json

# Create your views here.

def recommender(request):

    wiki_topic = request.GET['wiki_topic']

    wiki_text = wikiExtractor(wiki_topic)
    wiki_vector = article2Vec(wiki_text)
    response = json.dumps(list(wiki_vector))

    return HttpResponse(response)
