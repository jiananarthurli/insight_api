from django.shortcuts import render

from vectorizer.apps import event_matrix, idf_dict, key_tokens, event_matrix2list_dict, list2event_matrix_dict
from extractor.views import wikiExtractor
from vectorizer.views import tf_idf
from recommender.models import EventList

from django.http import HttpResponse
import json
import numpy as np

from time import time

# Create your views here.


def predict(event_matrix, vec_norm, threshold):

    prod = vec_norm.dot(event_matrix.T)
    # returned values are the indices of the SELECTED events, or the event matrix indices
    event_pred = list(np.nonzero(prod[0, :] > threshold)[0])

    return event_pred


# The actual recommender function that take http requests and return results.
# Threshold is hard coded.
# The event matrix is pre-calculated
def recommender(request):

    threshold = 0.235

    wiki_topic = request.GET['wiki_topic']
    wiki_text = wikiExtractor(wiki_topic)

    tic = time()

    # obtain vector for the wiki article
    wiki_vec = tf_idf(wiki_text, key_tokens, idf_dict)

    # recommendation list
    recommendations = predict(event_matrix, wiki_vec.reshape(1, -1), threshold)

    found = False # updated to True if events are found
    recommendation_list = []

    # if recommendations are found, find events in the list and construct the response dict
    if len(recommendations) != 0:
        found = True
        for ix in recommendations:
            event_ix = int(event_matrix2list_dict[str(ix)])
            event_object = EventList.objects.get(index=event_ix)
            event_name = event_object.name
            event_link = event_object.link
            event_venue = event_object.venue

            recommendation_list.append({
                'name' : event_name,
                'link' : event_link,
                'venue' : event_venue
            })

    response_dict = {
        'found' : found,
        'events' : recommendation_list
    }

    response = json.dumps(response_dict)

    print("Time lapse {}".format(time() - tic))

    return HttpResponse(response)
