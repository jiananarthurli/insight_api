from django.shortcuts import render
from vectorizer.apps import emb, emb_dim
from recommender.apps import events_list
from vectorizer.views import article2Vec
from extractor.views import wikiExtractor

from django.http import HttpResponse
import json
import numpy as np

# Create your views here.


def recommender(request):

    wiki_topic = request.GET['wiki_topic']

    wiki_text = wikiExtractor(wiki_topic)
    wiki_vector = article2Vec(wiki_text)

    event_matrix = np.zeros((emb_dim, len(events_list)))

    for i, event in enumerate(events_list):
        event_matrix[:, i] = article2Vec(event['description'])

    event_ix = np.argmax(event_matrix.T.dot(wiki_vector))

    response_dict = {
        'found' : True,
        'events' : events_list[event_ix:event_ix+2] # top 3
    }

    response = json.dumps(response_dict)

    return HttpResponse(response)
